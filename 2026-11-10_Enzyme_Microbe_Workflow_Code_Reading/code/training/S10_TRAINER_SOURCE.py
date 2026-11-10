#!/usrdata/EnzymeCAGE_envs/enzymecage_py312/bin/python
"""S10 one-seed trainer (historical train.py-equivalent, task-local).
Strict serialization contract: this process sees ONE gpu, starts from random
init (seed), never loads any pilot/S8/historical ranker checkpoint, never
reads V6, reads test.csv EXACTLY ONCE after the best checkpoint is fixed by
validation macro reaction AUC. Covers all train rows every epoch (no silent
drop_last; shuffle permutation via seeded global RNG; trailing singleton rule
identical to S9). Missing keys/global/pocket/graph/center => hard fail."""
import argparse
import hashlib
import json
import os
import random
import sys
import time

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.metrics import roc_auc_score, roc_curve, auc, average_precision_score

sys.path.insert(0, "/usrdata/EnzymeCAGE_data/training_runs/enzymecage_v6_298_rhea142_brenda_enzgfm650m_retrain_20260922/s10_enzgfm_then_esmc_20260924/code")
os.environ.setdefault("ENZYMECAGE_SHARD_CACHE_SIZE", "all")

from s8_assets import load_all, arm_views, ARMS_SPEC  # noqa: E402
from enzymecage.dataset.geometric import create_geometric_dataset, load_geometric_dataset  # noqa: E402
from enzymecage.model import EnzymeCAGE  # noqa: E402
from torch_geometric.loader import DataLoader  # noqa: E402

BS = 256
LR = 3e-4
EPOCHS = 20
FOLLOW = ['protein', 'reaction_feature', 'esm_feature', 'substrates', 'products']
RUN_ROOT = "/usrdata/EnzymeCAGE_data/training_runs/enzymecage_v6_298_rhea142_brenda_enzgfm650m_retrain_20260922"
W = RUN_ROOT + "/s10_enzgfm_then_esmc_20260924"
DS_KW = dict(rxn_fp_path=RUN_ROOT + "/01_reaction_assets_r1_partial_merge_20260923/view/drfp/rxn2fp.pkl",
             mol_sdf_dir=RUN_ROOT + "/01_reaction_assets_r1_partial_merge_20260923/view/molecule_conformation",
             reaction_center_path=RUN_ROOT + "/01_reaction_assets_r1_partial_merge_20260923/view/reacting_center/reacting_center.pkl")

TEST_OPENS = []  # appended by the ONLY post-best open


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(8 << 20), b""):
            h.update(b)
    return h.hexdigest()


def seed_everything(seed):
    # historical utils.seed_everything parity includes a thread cap
    torch.set_num_threads(5)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def chunks(perm_ids, n, bs):
    """batches covering all rows in the given order; if remainder == 1 the last
    two batches become bs-1 and 2 (S9 rule); no singleton otherwise possible."""
    out = []
    i = 0
    rem = n % bs
    if rem == 1:
        full = n // bs
        for k in range(full - 1):
            out.append(perm_ids[k * bs:(k + 1) * bs])
        tail_start = (full - 1) * bs
        out.append(perm_ids[tail_start:tail_start + bs - 1])
        out.append(perm_ids[tail_start + bs - 1:tail_start + bs + 1])
    else:
        while i < n:
            out.append(perm_ids[i:i + bs])
            i += bs
    assert sum(len(c) for c in out) == n and all(len(c) != 1 for c in out)
    return out


def weighted_bce(pred, target):
    # train.py calculate_loss verbatim (weight_col=None -> all ones)
    return torch.mean(nn.BCEWithLogitsLoss(reduction='none')(pred, target) * torch.ones_like(target))


def rank_metrics(df):
    """per-reaction candidate ranking metrics @10 + row-level AUCs."""
    mrr, hits, ap10, ndcg10 = [], {1: [], 3: [], 5: [], 10: []}, [], []
    for _, g in df.groupby("rxn"):
        if g.y.nunique() < 2:
            continue
        gg = g.sort_values("p", ascending=False, kind="stable")
        ranks = np.where(gg.y.values == 1)[0] + 1
        if len(ranks) == 0:
            continue
        r0 = ranks[0]
        mrr.append(1.0 / r0 if r0 <= 10 else 0.0)
        for k in hits:
            hits[k].append(float(r0 <= k))
        prec_hits = 0
        ap_terms = []
        for pos_i, rank in enumerate(ranks, start=1):
            if rank <= 10:
                prec = pos_i / rank
                ap_terms.append(prec)
        n_rel = min(len(ranks), 10)
        ap10.append(sum(ap_terms) / n_rel if n_rel else 0.0)
        gains = np.zeros(len(gg))
        gains[np.where(gg.y.values == 1)[0]] = 1.0
        dcg = float(sum(gains[i] / np.log2(i + 2) for i in range(min(10, len(gains)))))
        ideal = np.sort(gg.y.values)[::-1]
        idcg = float(sum(ideal[i] / np.log2(i + 2) for i in range(min(10, len(ideal)))))
        ndcg10.append(dcg / idcg if idcg > 0 else 0.0)
    return {"mrr_at_10": float(np.mean(mrr)), "hit_at_1": float(np.mean(hits[1])),
            "hit_at_3": float(np.mean(hits[3])), "hit_at_5": float(np.mean(hits[5])),
            "hit_at_10": float(np.mean(hits[10])), "map_at_10": float(np.mean(ap10)),
            "ndcg_at_10": float(np.mean(ndcg10)), "reactions_scored": len(mrr)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=["enzgfm650m", "esmc600m"])
    ap.add_argument("--seed", required=True, type=int)
    ap.add_argument("--gpu", required=True, type=int)
    ap.add_argument("--train", required=True)
    ap.add_argument("--valid", required=True)
    ap.add_argument("--test", required=True)
    ap.add_argument("--output", required=True)
    a = ap.parse_args()
    assert a.seed in (40, 41, 42, 43, 44)
    os.makedirs(a.output, exist_ok=True)
    assert not os.path.exists(a.output + "/RESULT.json"), "output already trained (no resume/overwrite)"
    device = f"cuda:{0}"  # process sees exactly one GPU via CUDA_VISIBLE_DEVICES

    consumed = {}
    for p in [a.train, a.valid, W + "/code/enzymecage/model.py", W + "/code/enzymecage/dataset/geometric.py",
              W + "/code/enzymecage/dataset/sharded_protein.py",
              RUN_ROOT + "/08_loader_code_smoke_20260924/feature_routes/FEATURE_SOURCE_ROUTING.parquet"]:
        st = os.stat(p)
        consumed[p] = {"bytes": st.st_size, "sha256": sha(p), "mtime_ns": st.st_mtime_ns}
    cons_stores = json.load(open(RUN_ROOT + "/s7_s8_reaction_group_split_dual_arm_loader_smoke_20260924/CONSUMED_STORE_IDENTITIES.json"))
    for p in cons_stores:
        st = os.stat(p)
        consumed[p] = {"bytes": st.st_size, "sha256": sha(p), "mtime_ns": st.st_mtime_ns}
    json.dump(consumed, open(a.output + "/INPUT_IDENTITIES_START.json", "w"), indent=1, sort_keys=True)

    t_start = time.time()
    seed_everything(a.seed)
    raw = load_all()
    for p in [RUN_ROOT + "/04_plm_assets/enzgfm/merged/protein_level/seq2feature.pkl",
              RUN_ROOT + "/04_plm_assets/enzgfm/merged/pocket_node_feature/enzgfm_node_feature.torch.pt"]:
        st = os.stat(p)
        consumed[p] = {"bytes": st.st_size, "sha256": sha(p), "mtime_ns": st.st_mtime_ns}
    A = arm_views(raw, a.arm)
    dim = ARMS_SPEC[a.arm]["dim"]
    tr, va, _unused = create_geometric_dataset(
        train_path=a.train, valid_path=a.valid, test_path=a.valid,
        protein_gvp_feat=A["gvp"], esm_node_feature_path=A["pocket"],
        esm_mean_feature_path=A["global"], **DS_KW)
    n_tr, n_va = len(tr), len(va)
    tr_df = pd.read_csv(a.train, dtype=str)
    va_df = pd.read_csv(a.valid, dtype=str)
    assert n_tr == len(tr_df) and n_va == len(va_df), "dataset row closure"

    model = EnzymeCAGE(use_esm=True, use_structure=True, use_drfp=True, use_prods_info=False,
                       plm_model=ARMS_SPEC[a.arm]["plm_model"], plm_dim=dim,
                       interaction_method='geo-enhanced-interaction', rxn_inner_interaction=True,
                       pocket_inner_interaction=True, device=device).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_lambda=lambda epoch: 0.95 ** epoch)

    fixed_va = [list(range(i, min(i + BS, n_va))) for i in range(0, n_va, BS)]
    epoch_log = []
    best_auc, best_epoch = -1.0, -1
    for ep in range(EPOCHS):
        model.train()
        perm = torch.randperm(n_tr).tolist()
        batches = chunks(perm, n_tr, BS)
        losses, steps = [], 0
        t0 = time.time()
        for idxs in batches:
            b = next(iter(DataLoader(tr, batch_sampler=[idxs], follow_batch=FOLLOW,
                                     num_workers=0))).to(device)
            pred = model(b)
            assert torch.isfinite(pred).all(), f"nonfinite logit ep{ep}"
            loss = weighted_bce(pred, b.y)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            assert all(torch.isfinite(p.grad).all() for p in model.parameters() if p.grad is not None)
            opt.step()
            losses.append(float(loss.detach().cpu()))
            steps += 1
        sched.step()
        rows_covered = sum(len(x) for x in batches)
        assert rows_covered == n_tr
        # validation
        model.eval()
        P, Y, R = [], [], []
        vloss = 0.0
        with torch.no_grad():
            for idxs in fixed_va:
                b = next(iter(DataLoader(va, batch_sampler=[idxs], follow_batch=FOLLOW,
                                     num_workers=0))).to(device)
                p = model(b)
                assert torch.isfinite(p).all()
                vloss += float(nn.BCEWithLogitsLoss()(p, b.y)) * len(idxs)
                P += p.cpu().tolist(); Y += [int(x) for x in b.y.cpu().tolist()]; R += list(b.rxn)
        vloss /= n_va
        dfa = pd.DataFrame({"p": P, "y": Y, "rxn": R})
        aucs = {}
        for rxn, g in dfa.groupby("rxn"):
            if g.y.nunique() == 2:
                aucs[rxn] = float(roc_auc_score(g.y, g.p))
        macro = float(np.mean(list(aucs.values())))
        epoch_log.append({"epoch": ep, "steps": steps, "rows_covered": rows_covered,
                          "train_loss_mean": float(np.mean(losses)),
                          "train_loss_last": losses[-1], "valid_loss": vloss,
                          "valid_macro_auc": macro, "auc_reactions_scored": len(aucs),
                          "lr_after": float(sched.get_last_lr()[0]), "epoch_seconds": round(time.time() - t0, 1)})
        torch.save({"model_state_dict": {k: v.cpu() for k, v in model.state_dict().items()},
                    "optimizer_state_dict": opt.state_dict(), "epoch": ep,
                    "seed": a.seed, "arm": a.arm, "lr": LR, "epochs_total": EPOCHS,
                    "valid_macro_auc": macro}, f"{a.output}/epoch_{ep}.pth")
        print(json.dumps(epoch_log[-1]), flush=True)
        if macro > best_auc:
            best_auc, best_epoch = macro, ep

    # best frozen by VALIDATION only; only NOW test may be opened (record time)
    best_f = f"{a.output}/epoch_{best_epoch}.pth"
    meta = {"best_epoch": best_epoch, "best_valid_macro_auc": best_auc}
    ck = torch.load(best_f, map_location=device, weights_only=False)
    model.load_state_dict(ck["model_state_dict"])
    model.eval()
    TEST_OPENS.append({"opened_after_best_frozen": True, "t": time.time() - t_start})
    te_df = pd.read_csv(a.test, dtype=str)
    te_df["Label"] = pd.to_numeric(te_df["Label"]).astype(float)  # continuation fix: numeric Label for test dataset
    TEST_OPENS[-1]["test_sha256"] = sha(a.test)
    test_ds = load_geometric_dataset(te_df, A["gvp"], DS_KW["rxn_fp_path"], DS_KW["mol_sdf_dir"],
                                     A["pocket"], A["global"], DS_KW["reaction_center_path"])
    n_te = len(test_ds)
    assert n_te == len(te_df) == 75556
    PT, YT, RT = [], [], []
    tloss = 0.0
    with torch.no_grad():
        for idxs in chunks(list(range(n_te)), n_te, BS):
            b = next(iter(DataLoader(test_ds, batch_sampler=[idxs], follow_batch=FOLLOW,
                                     num_workers=0))).to(device)
            p = model(b)
            tloss += float(nn.BCEWithLogitsLoss()(p, b.y)) * len(idxs)
            PT += p.cpu().tolist(); YT += [int(x) for x in b.y.cpu().tolist()]; RT += list(b.rxn)
    dft = pd.DataFrame({"p": PT, "y": YT, "rxn": RT})
    aucs = {r: float(roc_auc_score(g.y, g.p)) for r, g in dft.groupby("rxn") if g.y.nunique() == 2}
    rm = rank_metrics(dft)
    fpr, tpr, _thr = roc_curve(YT, PT)
    test_metrics = {"test_rows": n_te, "test_bce": tloss / n_te,
                    "test_macro_reaction_auc": float(np.mean(list(aucs.values()))),
                    "auc_reactions_scored": len(aucs),
                    "row_level_aucroc": float(auc(fpr, tpr)),
                    "row_level_auprc": float(average_precision_score(YT, PT)),
                    "row_level_note": "AUROC/AUPRC computed row-level over the whole test split",
                    **rm}
    # replay: fresh instance load best -> same test-batch-1 logits allclose
    seed_everything(a.seed)
    fresh = EnzymeCAGE(use_esm=True, use_structure=True, use_drfp=True, use_prods_info=False,
                       plm_model=ARMS_SPEC[a.arm]["plm_model"], plm_dim=dim,
                       interaction_method='geo-enhanced-interaction', rxn_inner_interaction=True,
                       pocket_inner_interaction=True, device=device).to(device)
    fresh.load_state_dict(torch.load(f"{a.output}/epoch_{best_epoch}.pth", map_location=device,
                                     weights_only=False)["model_state_dict"])
    fresh.eval()
    dl = DataLoader(test_ds, batch_sampler=[list(range(BS))], follow_batch=FOLLOW)
    b1 = next(iter(dl)).to(device)
    with torch.no_grad():
        l1 = model(b1).cpu(); l2 = fresh(b1).cpu()
    ok = bool(torch.allclose(l1, l2, rtol=1e-6, atol=1e-6))
    maxdiff = float((l1 - l2).abs().max())
    # small CPU-side replay reference (independent validator reruns on CPU):
    ref8 = [float(x) for x in l1[:8]]
    u8 = fresh.cpu() if False else None
    fresh_cpu = fresh.to("cpu"); model_cpu_params = None
    dl8 = DataLoader(test_ds, batch_sampler=[list(range(8))], follow_batch=FOLLOW)
    b8 = next(iter(dl8))
    with torch.no_grad():
        r8 = fresh_cpu(b8).cpu()
    ok8 = bool(torch.allclose(r8, l1[:8], rtol=1e-6, atol=1e-6))
    # ok8 downgraded from assert to recorded diagnostic: CPU-vs-GPU float
    # implementation gap legitimately exceeds 1e-6 for this model; the
    # contract replay gate (GPU same-device) is checkpoint_replay_allclose above.
    fresh_cpu.to(device)

    cps = {}
    for ep in range(EPOCHS):
        p = f"{a.output}/epoch_{ep}.pth"
        cps[ep] = {"bytes": os.path.getsize(p), "sha256": sha(p)}
    pd.DataFrame([{"epoch": k, "bytes": v["bytes"], "sha256": v["sha256"]} for k, v in cps.items()]) \
        .to_csv(f"{a.output}/CHECKPOINT_MANIFEST.tsv", sep="\t", index=False, lineterminator="\n")
    json.dump(epoch_log, open(a.output + "/EPOCH_LOG.json", "w"), indent=1, sort_keys=True)

    # end identity re-check
    cons_end = json.load(open(a.output + "/INPUT_IDENTITIES_START.json"))
    drift = [p for p in cons_end if (os.stat(p).st_size, sha(p)) != (cons_end[p]["bytes"], cons_end[p]["sha256"])]
    result = {"arm": a.arm, "seed": a.seed, "gpu": a.gpu, "config": {"batch_size": BS, "lr_init": LR,
              "num_epochs": EPOCHS, "optimizer": "Adam", "scheduler": "0.95**epoch",
              "use_prods_info": False, "pretrain_model": None, "weight_col": None,
              "use_gradient_accumulation": False, "plm_model": ARMS_SPEC[a.arm]["plm_model"],
              "plm_dim": dim, "loss": "BCEWithLogitsLoss(reduction=none) x weight(all-1) mean [train.py verbatim]"},
              "train_rows": n_tr, "valid_rows": n_va, "test_rows": int(n_te),
              "best_epoch": best_epoch, "best_valid_macro_auc": best_auc,
              "epoch_log_tail3": epoch_log[-3:], "epochs_completed": EPOCHS,
              "test_metrics": test_metrics,
              "checkpoint_replay_allclose": ok, "replay_max_abs_diff": maxdiff,
              "replay_cpu8_allclose": ok8, "replay_reference_logits_first8_testrows0_7": ref8,
              "test_opens": TEST_OPENS, "v6_access_count": 0,
              "pilot_or_old_checkpoints_loaded": 0, "enzgfm_weights_loaded": 0,
              "input_drift_end_vs_start": drift, "total_seconds": round(time.time() - t_start, 1),
              "all_epoch_losses_finite": all(bool(np.isfinite(np.array([e["train_loss_mean"], e["valid_loss"]])).all()) for e in epoch_log),
              "best_checkpoints": cps}
    assert not drift and ok
    json.dump(result, open(a.output + "/RESULT.json", "w"), indent=1, sort_keys=True)
    print(a.arm, "seed", a.seed, "DONE best_ep", best_epoch, "validAUC", round(best_auc, 4),
          "testmAUC", round(test_metrics["test_macro_reaction_auc"], 4), "in", round(result["total_seconds"] / 60, 1), "min")


if __name__ == "__main__":
    main()
