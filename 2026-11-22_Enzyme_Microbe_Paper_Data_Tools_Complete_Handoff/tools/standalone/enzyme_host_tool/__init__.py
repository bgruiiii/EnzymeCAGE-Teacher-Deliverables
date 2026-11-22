"""Standalone enzyme/host prediction tool (R2: final binding & status).

Contract (user-fixed, unchanged): Top-10 similar reaction GROUPS recall
candidate enzymes; the ORIGINAL target reaction is scored against every
candidate; full ordering follows the wrapper rule (-score, uid) with Top-K as
display only; all associated UIDs resolve hosts via the B1 authoritative
source_signature; traits keep per-backend status with t6_prod conservative
slot rules; CACHE_REPLAY requires strict arm/step/key binding — never a
first/last guess, never cross-step borrowing. No depending imports, no .env,
no mock scores on live paths, no cluster submissions.
"""
from .config import ToolConfig
from .predict import predict_reaction, predict_steps

__all__ = ["ToolConfig", "predict_reaction", "predict_steps"]
__version__ = "0.3.0-r2-binding"
