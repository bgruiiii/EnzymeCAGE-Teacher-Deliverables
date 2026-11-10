import os
import json
import argparse
import yaml
import time
import resource

from tqdm import tqdm
import torch
from torch import nn
from torch_geometric.loader import DataLoader
from rdkit import RDLogger
RDLogger.logger().setLevel(RDLogger.ERROR)

from config import Config
from enzymecage.model import EnzymeCAGE
from enzymecage.dataset.geometric import create_geometric_dataset
from enzymecage.dataset.baseline import create_baseline_dataset
from enzymecage.baseline import Baseline
from utils import seed_everything, check_files

TARGET_BATCH_SIZE = 256

WEIGHT_PRINT_FLAG = False


def get_accumulation_steps(batch_size):
    if batch_size >= TARGET_BATCH_SIZE // 2:
        accumulation_steps = 1
    else:
        accumulation_steps = TARGET_BATCH_SIZE // batch_size
    return accumulation_steps


def backup_config(config_path, save_dir=None):
    with open(config_path, "r", encoding="utf-8") as fp:
        conf_dict = yaml.load(fp, Loader=yaml.FullLoader)
        
    ckpt_dir = conf_dict["ckpt_dir"] if save_dir is None else save_dir
    if not os.path.exists(ckpt_dir):
        os.makedirs(ckpt_dir)
        
    save_path = os.path.join(ckpt_dir, "config.yaml")
    with open(save_path, "w", encoding="utf-8") as fp:
        yaml.dump(conf_dict, fp)


def calculate_loss(loss_func, pred, target, batch_data):
        if hasattr(batch_data, 'weight'):
            weight = batch_data.weight
        else:
            weight = torch.ones_like(target)
        
        global WEIGHT_PRINT_FLAG
        if not WEIGHT_PRINT_FLAG:
            WEIGHT_PRINT_FLAG = True
            print(f'weights: {weight}')
            
        weighted_loss = loss_func(pred, target) * weight
        return torch.mean(weighted_loss)


def _feature_shape(value):
    if hasattr(value, 'shape'):
        return tuple(value.shape)
    return tuple(torch.as_tensor(value).shape)


def validate_esm_feature_contract(datasets, model):
    expected_dim = model.esm_dim
    failures = []

    for split_name, dataset in datasets.items():
        if hasattr(dataset, 'esm_dim') and dataset.esm_dim != expected_dim:
            failures.append(
                f'{split_name}: pocket ESM dim {dataset.esm_dim} != model dim {expected_dim}'
            )

        unique_uids = sorted(set(dataset.uniprot_ids))
        unique_seqs = sorted(set(dataset.seqs))

        if model.use_esm:
            if not dataset.esm_feat_dict:
                failures.append(f'{split_name}: missing sequence-level ESM feature dict')
            else:
                missing_seqs = [seq for seq in unique_seqs if seq not in dataset.esm_feat_dict]
                if missing_seqs:
                    failures.append(
                        f'{split_name}: {len(missing_seqs)} sequences missing in seq2feature.pkl'
                    )
                for seq in unique_seqs:
                    if seq not in dataset.esm_feat_dict:
                        continue
                    shape = _feature_shape(dataset.esm_feat_dict[seq])
                    if shape != (expected_dim,):
                        failures.append(
                            f'{split_name}: sequence feature shape {shape} != ({expected_dim},)'
                        )
                        break

        if model.use_structure:
            missing_uids = [uid for uid in unique_uids if uid not in dataset.pocket_node_feature]
            if missing_uids:
                failures.append(
                    f'{split_name}: {len(missing_uids)} UIDs missing in pocket_node_feature'
                )
            for uid in unique_uids:
                if uid not in dataset.pocket_node_feature:
                    continue
                pocket_shape = _feature_shape(dataset.pocket_node_feature[uid])
                if len(pocket_shape) != 2 or pocket_shape[1] != expected_dim:
                    failures.append(
                        f'{split_name}: {uid} pocket feature shape {pocket_shape} '
                        f'does not match [N,{expected_dim}]'
                    )
                    break
                protein_node_xyz = dataset.protein_dict[uid][0]
                if pocket_shape[0] != len(protein_node_xyz):
                    failures.append(
                        f'{split_name}: {uid} pocket/GVP node count mismatch '
                        f'ESM={pocket_shape[0]}, GVP={len(protein_node_xyz)}'
                    )
                    break

    if failures:
        preview = '\n'.join(failures[:20])
        raise ValueError(f'ESM feature contract validation failed:\n{preview}')

    print(f'ESM feature contract validation passed: dim={expected_dim}')


def main(model_conf):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # P1: Program/startup timing
    _run_start_time = time.perf_counter()
    _run_start_wall = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f'[TIMING] Program start: {_run_start_wall}')

    follow_batch = ['protein', 'reaction_feature', 'esm_feature', 'substrates', 'products']
    esm_model = None
    if hasattr(model_conf, 'esm_model'):
        esm_model = model_conf.esm_model
    model = EnzymeCAGE(
        use_esm=model_conf.use_esm,
        use_structure=model_conf.use_structure,
        use_drfp=model_conf.use_drfp,
        use_prods_info=model_conf.use_prods_info,
        esm_model=esm_model,
        interaction_method=model_conf.interaction_method,
        rxn_inner_interaction=model_conf.rxn_inner_interaction,
        pocket_inner_interaction=model_conf.pocket_inner_interaction,
        device=device
    )
    
    if hasattr(model_conf, 'pretrain_model') and model_conf.pretrain_model:
        if os.path.exists(model_conf.pretrain_model):
            pretrain_model = torch.load(model_conf.pretrain_model, map_location=device)
            model.load_state_dict(pretrain_model)
            print(f'Load pretrained model from {model_conf.pretrain_model}')
        else:
            raise FileNotFoundError(f'Pretrain model not found: {model.pretrain_model}')
    
    print('Model save dir: ', model_conf.ckpt_dir)

    weight_col = model_conf.weight_col if hasattr(model_conf, 'weight_col') else None
    print(f'Sample weight column: {weight_col}')
    
    # P1: Dataset + DataLoader construction timing
    _data_load_start = time.perf_counter()
    train_set, valid_set, test_set = create_geometric_dataset(train_path=model_conf.train_path,
                                                                valid_path=model_conf.valid_path,
                                                                test_path=model_conf.test_path,
                                                                protein_gvp_feat=model_conf.protein_gvp_feat, 
                                                                rxn_fp_path=model_conf.rxn_fp, 
                                                                mol_sdf_dir=model_conf.mol_conformation, 
                                                                esm_node_feature_path=model_conf.esm_node_feature, 
                                                                esm_mean_feature_path=model_conf.esm_mean_feature, 
                                                                reaction_center_path=model_conf.reaction_center,
                                                                weight_col=weight_col)
    validate_esm_feature_contract(
        {'train': train_set, 'valid': valid_set, 'test': test_set},
        model,
    )
    
    test_loader = DataLoader(test_set, batch_size=model_conf.batch_size, shuffle=False, follow_batch=follow_batch)
    valid_loader = DataLoader(valid_set, batch_size=model_conf.batch_size, shuffle=False, follow_batch=follow_batch)
    train_loader = DataLoader(train_set, batch_size=model_conf.batch_size, shuffle=True, follow_batch=follow_batch, drop_last=True)
    _data_load_end = time.perf_counter()
    _data_load_elapsed = _data_load_end - _data_load_start
    print(f'[TIMING] Dataset + DataLoader construction: {_data_load_elapsed:.1f}s ({_data_load_elapsed/60:.2f} min)')

    model.to(device)

    lr_init = model_conf.lr_init
    optimizer = torch.optim.Adam(model.parameters(), lr=lr_init)
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lambda epoch: 0.95 ** epoch)
    loss_func = nn.BCEWithLogitsLoss(reduction='none')

    os.makedirs(model_conf.ckpt_dir, exist_ok=True)

    # P1: Early stopping configuration
    early_stop_patience = getattr(model_conf, 'early_stop_patience', None)
    _no_improve_count = 0
    _best_epoch = -1
    _stop_epoch = -1
    _stop_reason = None

    best_metric = 0
    for epoch in range(model_conf.num_epochs):
        # P1: Epoch timing
        _epoch_start = time.perf_counter()
        _should_stop = False

        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
        print(f'================= Epoch {epoch} =================')
        loss_total = 0
        model.train()
        target_list = []
        pred_list = []
        all_rxns = []
        
        for _, batch in enumerate(tqdm(train_loader)):
            batch.epoch = epoch
            target = batch.y.to(device)
            batch.to(device)

            pred = model(batch)
            # loss = loss_func(pred, target)
            loss = calculate_loss(loss_func, pred, target, batch)
            
            loss.backward()            
            optimizer.step()
            optimizer.zero_grad()
            
            loss_total += loss.item()
            target_list.append(target.detach())
            pred_list.append(pred.detach())
            all_rxns.extend(batch.rxn)
        
        # P1: Training loop timing
        _train_loop_end = time.perf_counter()
        _train_loop_elapsed = _train_loop_end - _epoch_start
        print(f'[TIMING] Training loop: {_train_loop_elapsed:.1f}s ({_train_loop_elapsed/60:.2f} min)')

        # P1: Checkpoint save timing
        _ckpt_start = time.perf_counter()
        torch.save(model.state_dict(), os.path.join(model_conf.ckpt_dir, "epoch_%d.pth" % epoch))
        _ckpt_end = time.perf_counter()
        _ckpt_elapsed = _ckpt_end - _ckpt_start
        print(f'[TIMING] Epoch checkpoint save: {_ckpt_elapsed:.1f}s')

        lr = optimizer.state_dict()['param_groups'][0]['lr']
        n_step = len(train_loader)
        print(f"binary loss: {round(loss_total / n_step, 6)}, lr: {round(lr, 6)}\n")
        
        target_list = torch.concat(target_list)
        pred_list = torch.concat(pred_list)
        
        if not model.sigmoid_readout:
            pred_list = torch.sigmoid(pred_list)
                        
        train_metric = model.calc_metric(pred_list, target_list, all_rxns)
        for k, v in train_metric.items():
            print(f'Train {k}: {round(v, 4)}')
        print()

        model.eval()
        # P1: Validation timing
        _valid_start = time.perf_counter()
        _, valid_metric = model.evaluate(valid_loader)
        _valid_end = time.perf_counter()
        _valid_elapsed = _valid_end - _valid_start
        print(f'[TIMING] Validation: {_valid_elapsed:.1f}s ({_valid_elapsed/60:.2f} min)')

        for k, v in valid_metric.items():
            print(f'validation {k}: {round(v, 4)}')
        
        print()
        # P1: Test timing
        _test_start = time.perf_counter()
        _, test_metric = model.evaluate(test_loader)
        _test_end = time.perf_counter()
        _test_elapsed = _test_end - _test_start
        print(f'[TIMING] Test: {_test_elapsed:.1f}s ({_test_elapsed/60:.2f} min)')

        for k, v in test_metric.items():
            print(f'test {k}: {round(v, 4)}')
        
        early_stop_metric = valid_metric['AUC']

        if early_stop_metric > best_metric:
            best_metric = early_stop_metric
            _best_epoch = epoch
            # P1: Best checkpoint save timing
            _best_ckpt_start = time.perf_counter()
            best_model_path = os.path.join(model_conf.ckpt_dir, "best_model.pth")
            valid_metric_path = os.path.join(model_conf.ckpt_dir, "best_model_metrics_valid.json")
            test_metric_path = os.path.join(model_conf.ckpt_dir, "best_model_metrics_test.json")
            torch.save(model.state_dict(), best_model_path)
            print(f'Save best model to {best_model_path}')
            with open(valid_metric_path, 'w') as f:
                json.dump(valid_metric, f)
            with open(test_metric_path, 'w') as f:
                json.dump(test_metric, f)
            _best_ckpt_end = time.perf_counter()
            _best_ckpt_elapsed = _best_ckpt_end - _best_ckpt_start
            print(f'[TIMING] Best checkpoint save: {_best_ckpt_elapsed:.1f}s')
            _no_improve_count = 0
            print(f'[EARLY_STOP] Improved. best_epoch={_best_epoch}, best_valid_AUC={best_metric:.6f}, counter reset')
        else:
            _no_improve_count += 1
            print(f'[EARLY_STOP] No improvement. counter={_no_improve_count}/{early_stop_patience if early_stop_patience else "disabled"}')

        # P1: Early stopping check
        if early_stop_patience is not None and _no_improve_count >= early_stop_patience:
            _stop_epoch = epoch
            _stop_reason = f'{_no_improve_count} consecutive non-improving epochs (patience={early_stop_patience})'
            _should_stop = True

        # P1: Epoch-total timing
        _epoch_total = time.perf_counter() - _epoch_start
        print(f'[TIMING] Epoch {epoch} total: {_epoch_total:.1f}s ({_epoch_total/60:.2f} min)')

        # P1: Per-epoch resource observation
        try:
            _rusage = resource.getrusage(resource.RUSAGE_SELF)
            _rss_mb = _rusage.ru_maxrss / 1024
            print(f'[MEMORY] Max RSS: {_rss_mb:.1f} MB')
        except Exception as _e:
            print(f'[MEMORY] RSS observation failed: {_e}')

        if torch.cuda.is_available():
            _alloc = torch.cuda.memory_allocated() / 1024**3
            _reserved = torch.cuda.memory_reserved() / 1024**3
            _peak_alloc = torch.cuda.max_memory_allocated() / 1024**3
            _peak_reserved = torch.cuda.max_memory_reserved() / 1024**3
            print(f'[MEMORY] CUDA alloc: {_alloc:.2f} GiB, reserved: {_reserved:.2f} GiB, peak_alloc: {_peak_alloc:.2f} GiB, peak_reserved: {_peak_reserved:.2f} GiB')

        if _should_stop:
            print(f'\n[EARLY_STOP] Triggered at epoch {_stop_epoch}.')
            print(f'[EARLY_STOP] Best epoch: {_best_epoch}, best valid AUC: {best_metric:.6f}')
            print(f'[EARLY_STOP] Reason: {_stop_reason}')
            break

        if scheduler:
            scheduler.step()

        print()
    
    # P1: Final evaluation timing
    _final_eval_start = time.perf_counter()

    best_state_dict = torch.load(os.path.join(model_conf.ckpt_dir, "best_model.pth"))
    model.load_state_dict(best_state_dict)
    
    model.eval()
    print('\n================= Evaluate on Test =================')
    test_preds, metric = model.evaluate(test_loader)
    for k, v in metric.items():
        print(f'test {k}: {round(v, 4)}')
        
    df_test = test_set.df_data
    df_test['pred'] = test_preds.cpu()
    df_test.to_csv(os.path.join(model_conf.ckpt_dir, f"test_result.csv"), index=False)
    
    print('\n================= Evaluate on Valid again =================')
    valid_preds, metric = model.evaluate(valid_loader)
    for k, v in metric.items():
        print(f'valid {k}: {round(v, 4)}')
        
    df_valid = valid_set.df_data
    df_valid['pred'] = valid_preds.cpu()
    df_valid.to_csv(os.path.join(model_conf.ckpt_dir, f"valid_result.csv"), index=False)

    # P1: Final evaluation elapsed
    _final_eval_end = time.perf_counter()
    _final_eval_elapsed = _final_eval_end - _final_eval_start
    print(f'[TIMING] Final evaluation: {_final_eval_elapsed:.1f}s ({_final_eval_elapsed/60:.2f} min)')

    # P1: Run-total timing
    _run_end_time = time.perf_counter()
    _run_total = _run_end_time - _run_start_time
    print(f'\n[TIMING] Run total: {_run_total:.1f}s ({_run_total/60:.2f} min, {_run_total/3600:.2f} hours)')
    print(f'[TIMING] Run end: {time.strftime("%Y-%m-%d %H:%M:%S")}')
    if _stop_reason:
        print(f'[TIMING] Stopped at epoch {_stop_epoch}, reason: {_stop_reason}')


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True)
    args = parser.parse_args()
    
    assert os.path.exists(args.config)
    model_conf = Config(args.config)
    check_files(model_conf)
    
    seed = 42 if not hasattr(model_conf, 'seed') else model_conf.seed
    seed_everything(seed)
    backup_config(args.config)
    main(model_conf)
    
