"""Credential rotation layer for S8 runners. Keys never reach logs or archives.

Reads the user-owned local key doc; falls back to the legacy single token
file. Classification decides only HOW a failed request may be retried; it
never changes model, scoring content, ledger identity or dedup rules.
"""
import json
import re
from pathlib import Path

DOC = Path('/home/a/EnzymeCAGE/aliyun_scoring_api_keys.local.md')
LEGACY = Path('/home/a/EnzymeCAGE/apikey.tokenplan.ali1110.txt')

# Explicit quota/balance/no-permission style rejections that justify moving to
# the next credential of the same model, per the local key doc's usage terms.
SWITCH_PATTERNS = [
    'insufficient_quota', 'quota exhausted', 'quotaexhausted', 'exceeded your current quota',
    'arrearage', '欠费', '余额不足', '额度不足', '额度已用', 'balance', 'allocation has been exhausted',
    'invalidapikey', 'invalid_api_key', 'invalid api key', 'incorrect api key', 'api-key',
    'no access to model', 'model_not_found', 'model not found', 'do not have access',
    'not authorized', 'access denied', 'free allocated', 'quota limit', 'billing',
]


def load_credentials(expected_model=None):
    """Return ordered list of {alias, endpoint, base_url, key}; dedup by key.

    Empty/blank entries and enabled=false are skipped. If the doc yields
    nothing usable, fall back to the legacy token file as one alias.
    Raises if doc declares a different model than the pinned judge.
    """
    entries, doc_model = [], None
    if DOC.exists():
        m = re.search(r'```json\n(.*?)\n```', DOC.read_text(), re.S)
        if m:
            doc = json.loads(m.group(1))
            doc_model = doc.get('model')
            if expected_model and doc_model and doc_model != expected_model:
                raise RuntimeError('CREDENTIAL_DOC_MODEL_MISMATCH')
            for k in doc.get('keys', []):
                key = (k.get('api_key') or '').strip()
                if not k.get('enabled', True) or not key:
                    continue
                entries.append(dict(alias=str(k.get('id') or f'ali_{len(entries) + 1:02d}'),
                                    base_url=(k.get('base_url') or '').strip(), key=key))
    seen, out = set(), []
    for e in entries:
        if e['key'] in seen:
            continue
        seen.add(e['key'])
        e['endpoint'] = (e['base_url'].rstrip('/') + '/chat/completions') if e['base_url'] else None
        out.append(e)
    if not out and LEGACY.exists():
        key = LEGACY.read_text().strip()
        if key:
            out.append(dict(alias='legacy_token_file', base_url='', endpoint=None, key=key))
    return out


def classify(wire):
    """Pre-billing-safe retry class for one transport outcome.

    SWITCH        provably not-billed credential/quota/no-permission refusal
    BACKOFF       HTTP 429 rate limit (same credential, limited waits)
    PRE_DISPATCH  provable pre-upload local failure (retry; not key's fault)
    UNKNOWN_BILLED response may have been generated/billed: keep reserve, never re-buy
    REJECTED      scoring-side issue: never a key-switch reason
    """
    hs, ek = wire.get('http_status'), wire.get('error_kind') or ''
    if hs is None:
        if ek.startswith('PRE_DISPATCH'):
            return 'PRE_DISPATCH'
        return 'UNKNOWN_BILLED'
    if hs in (401, 403):
        return 'SWITCH'
    if hs == 429:
        return 'BACKOFF'
    if ek == 'SERVER_5XX':
        return 'UNKNOWN_BILLED'
    if 400 <= hs < 500:
        raw = wire.get('raw_response_bytes') or b''
        text = (raw.decode('utf-8', 'replace') if isinstance(raw, bytes) else str(raw)).lower()
        return 'SWITCH' if any(p in text for p in SWITCH_PATTERNS) else 'UNKNOWN_BILLED'
    return 'UNKNOWN_BILLED'


def scrub(text, secrets):
    """Remove any secret fragment before persisting an error excerpt."""
    s = str(text or '')
    for k in secrets:
        if k:
            s = s.replace(k, '***')
    return s[:220]
