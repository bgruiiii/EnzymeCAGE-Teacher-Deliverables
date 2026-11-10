"""Bound candidate batches while preserving legacy whole-step dense padding.

No checkpoint, feature, candidate, model layer, or sigmoid change. The legacy
model averages padded axes, so naive microbatches are NOT equivalent. Pin each
dense axis to its original entire-step maximum and run a real numerical
comparison before bulk inference. No torch import at module load (CPU tests).
"""
from contextlib import contextmanager
import json
import numpy as np


def _token(batch):
    return (int(batch.data_ptr()), int(batch.numel())) if hasattr(batch, 'data_ptr') else id(batch)


def step_caps(dataset):
    if not dataset.uniprot_ids:
        raise ValueError('EMPTY_FROZEN_POOL')
    protein = max(int(dataset.protein_dict[u][0].shape[0]) for u in dataset.uniprot_ids)
    first = dataset.get(0)
    return {'protein': protein, 'substrates': int(first['substrates'].num_nodes),
            'products': int(first['products'].num_nodes),
            'esm_feature': int(dataset.esm_dim), 'reaction_feature': 2048}


@contextmanager
def frozen_padding(model_module, data, caps):
    original = model_module.to_dense_batch
    declared = {}
    for family in ('protein', 'substrates', 'products'):
        declared[_token(data[family].batch)] = caps[family]
    declared[_token(data.esm_feature_batch)] = caps['esm_feature']
    declared[_token(data.reaction_feature_batch)] = caps['reaction_feature']
    def dense(x, batch=None, *args, **kwargs):
        key = _token(batch)
        if key not in declared:
            raise RuntimeError('UNREGISTERED_DENSE_BATCH_AXIS')
        want = declared[key]
        if kwargs.get('max_num_nodes') not in (None, want):
            raise RuntimeError('DENSE_PADDING_CONTRACT_CONFLICT')
        kwargs['max_num_nodes'] = want
        return original(x, batch, *args, **kwargs)
    model_module.to_dense_batch = dense
    try:
        yield
    finally:
        model_module.to_dense_batch = original


def forward_dataset(model, dataset, loader_class, follow, device, model_module,
                    max_candidates=16, caps=None):
    import torch
    if max_candidates < 1:
        raise ValueError('INVALID_CANDIDATE_BATCH_SIZE')
    caps = caps or step_caps(dataset)
    outputs = []
    loader = loader_class(dataset, batch_size=max_candidates, shuffle=False, follow_batch=follow)
    for data in loader:
        data = data.to(device)
        with frozen_padding(model_module, data, caps), torch.no_grad():
            value = model.forward(data)
        if isinstance(value, tuple):
            value = value[0]
        raw = value.detach().cpu().to(torch.float64).numpy().reshape(-1)
        if not np.isfinite(raw).all():
            raise RuntimeError('NON_FINITE_RAW_LOGIT')
        outputs.append(raw)
        del data, value
    values = np.concatenate(outputs) if outputs else np.array([], dtype=np.float64)
    if len(values) != len(dataset.uniprot_ids):
        raise RuntimeError('BOUNDED_FORWARD_MEMBERSHIP_LENGTH_DRIFT')
    return values


def real_invariance_smoke(model, build, step, loader_class, follow, device,
                          model_module, out_file, atol=1e-5, rtol=1e-5):
    """Old pure batch versus pinned microbatches on a fixed, score-blind sample.

    Include the largest protein graph so the sample has the full-step padding
    maximum. Reaction graphs and feature widths are identical for the step.
    This MUST run with the actual deployment/checkpoint, never with a stub.
    """
    import torch
    whole = build(step['model_reaction'], step['pool_uids'])
    caps = step_caps(whole)
    largest = max(range(len(whole.uniprot_ids)),
                  key=lambda i: int(whole.protein_dict[whole.uniprot_ids[i]][0].shape[0]))
    indices = sorted(set(range(min(8, len(whole.uniprot_ids)))) | {largest})
    uids = [whole.uniprot_ids[i] for i in indices]
    sample = build(step['model_reaction'], uids)
    data = next(iter(loader_class(sample, batch_size=len(uids), shuffle=False, follow_batch=follow))).to(device)
    with torch.no_grad():
        value = model.forward(data)
    if isinstance(value, tuple):
        value = value[0]
    reference = value.detach().cpu().to(torch.float64).numpy().reshape(-1)
    del data, value
    actual = forward_dataset(model, sample, loader_class, follow, device,
                             model_module, max_candidates=3, caps=caps)
    maximum = float(np.max(np.abs(reference-actual))) if len(actual) else 0.
    ok = bool(np.isfinite(reference).all() and np.allclose(reference, actual, atol=atol, rtol=rtol))
    report = {'step_id': step['step_id'], 'sample_candidates': len(uids), 'sample_indices': indices,
              'whole_step_candidates': len(whole.uniprot_ids), 'padding_caps': caps,
              'atol': atol, 'rtol': rtol, 'max_abs_raw_logit_delta': maximum,
              'pass': ok, 'synthetic': False, 'sigmoid_calls': 0}
    with open(out_file, 'w') as f:
        json.dump(report, f, indent=2)
    if not ok:
        raise RuntimeError('REAL_BATCH_INVARIANCE_SMOKE_FAILED_BEFORE_BULK')
    return report
