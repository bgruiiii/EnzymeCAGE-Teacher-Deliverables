"""CPU helpers for the R3 source-recovery fixes. No model/GPU imports."""
import hashlib
import json
import os
from contextlib import contextmanager
from pathlib import Path


def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(4 << 20), b''):
            h.update(block)
    return h.hexdigest()


def recovery_bundles(package):
    root = Path(package) / 'recovery109'
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    out = {}
    for uid, r in manifest.items():
        item = dict(r)
        for key in ('pdb', 'pocket_ok', 'gvp'):
            rel = Path(r[key])
            if rel.is_absolute() or '..' in rel.parts:
                raise ValueError('RECOVERY_PATH_ESCAPE')
            path = root / rel
            if sha_file(path) != r[key + '_sha256']:
                raise ValueError('RECOVERY_BODY_DRIFT:' + uid + ':' + key)
            item[key] = str(path)
        if hashlib.sha256(json.dumps(r['indices']).encode()).hexdigest() != r['indices_sha256']:
            raise ValueError('RECOVERY_INDICES_DRIFT:' + uid)
        if len(r['indices']) != r['rows'] or not r['indices']:
            raise ValueError('RECOVERY_ROW_CONTRACT:' + uid)
        out[uid] = item
    return out


@contextmanager
def a109_overlay_context(a109_root, ctx):
    """Scope the original accepted overlay to 3B construction, never 600M."""
    gf = json.loads((Path(a109_root) / 'ctx' / (ctx + '.gf.json')).read_text())
    cp = gf['r2_context']
    rc = json.loads(Path(cp).read_text())
    for key in ('registry', 'pocket_overlay_dir', 'gvp_overlay_dir'):
        if not Path(rc[key]).exists():
            raise FileNotFoundError('A109_OVERLAY_INPUT_MISSING:' + key + ':' + rc[key])
    prior = os.environ.get('C95_R2_1_CONTEXT')
    os.environ['C95_R2_1_CONTEXT'] = cp
    try:
        yield rc
    finally:
        if prior is None:
            os.environ.pop('C95_R2_1_CONTEXT', None)
        else:
            os.environ['C95_R2_1_CONTEXT'] = prior


def build_3b_index(paths, ctx, config, base_class, extended_class):
    with a109_overlay_context(paths.A109, ctx):
        return extended_class(base_class(config), paths.PKG + '/inputs/' + ctx + '/RUNTIME_SEQUENCE_PARENT.tsv')


def a109_identity(paths, ctx):
    gfpath = Path(paths.A109) / 'ctx' / (ctx + '.gf.json')
    gf = json.loads(gfpath.read_text())
    rc = json.loads(Path(gf['r2_context']).read_text())
    return {'gf_context_sha256': sha_file(gfpath), 'overlay_context_sha256': sha_file(gf['r2_context']),
            'registry_sha256': sha_file(rc['registry']),
            'quarantine_sha256': sha_file(rc['quarantine']) if rc.get('quarantine') and Path(rc['quarantine']).is_file() else None}


def actual_gvp(uid, source, paths, torch_module, store_loader, cache):
    """Read rows from the real value; metadata None is never structural absence."""
    if source == 'FLAT_JULY':
        filename = paths.STORES['gvp_flat']
        if filename not in cache:
            cache[filename] = store_loader(filename)
    elif source == 'S3_SEPT':
        filename = paths.STORES['gvp_s3_new']
        if filename not in cache:
            cache[filename] = torch_module.load(filename, map_location='cpu', weights_only=False)
    elif source == 'R1_SEPT':
        filename = paths.STORES['gvp_r1_overlay']
        if filename not in cache:
            cache[filename] = torch_module.load(filename, map_location='cpu', weights_only=False)
    else:
        raise ValueError('UNREGISTERED_GVP_STORE:' + source)
    value = cache[filename][uid]
    n = int(value[0].shape[0])
    if n <= 0 or len(value) != 7:
        raise ValueError('GVP_BODY_CONTRACT:' + uid)
    return value, n, filename


def require_scoring_gate(pool_dir):
    """Checked before model import/loading; asset repair and PC are separate."""
    gate_path = Path(pool_dir) / 'ALL_MODELS_ASSETS_READY.json'
    if not gate_path.is_file():
        raise RuntimeError('SCORING_FORBIDDEN_UNTIL_ALL_FIVE_MODELS_ASSETS_READY')
    gate = json.loads(gate_path.read_text())
    wanted = {'legacy_esm2_3b', 'legacy_esmc600m', 'new_esmc600m', 'current_e0_enzgfm650m', 'new_enzgfm650m'}
    if gate.get('status') != 'ALL_MODELS_ASSETS_READY' or set(gate.get('arms', [])) != wanted or gate.get('steps') != 382:
        raise RuntimeError('SCORING_GATE_SCOPE_MISMATCH')
    if sha_file(gate['consumer_ledger_path']) != gate['consumer_ledger_sha256']:
        raise RuntimeError('SCORING_GATE_LEDGER_DRIFT')
    for ctx in ('main', 'delta15'):
        if sha_file(Path(pool_dir) / f'UNIFIED_STEP_TABLE_{ctx}.json') != gate['step_table_sha256'][ctx]:
            raise RuntimeError('SCORING_GATE_POOL_DRIFT:' + ctx)
    return gate
