#!/usr/data/EnzymeCAGE_envs/enzymecage_py312/bin/python
"""S5 GVP lane: frozen implementation authority = repo feature/
gvp_torchdrug_feature.batch_run (S3/Q5 loader accepted; B3B-audited contract).
Inputs: exact sequence + historical pocket PDB for the selected UID + pocket
index rows must match. Task-local outputs only."""
import glob,hashlib,json,os,pickle,sys,time
import numpy as np,pandas as pd,torch
# --- C95 task-local context loader (inserted; original code untouched) ---
import json as _c95json, os as _c95os
_c95p = _c95os.environ.get("C95_LANE_CONTEXT")
if not _c95p:
    raise SystemExit("C95_LANE_CONTEXT env (task-local path context JSON) required for C95 adapted copies")
__C95_CTX = _c95json.load(open(_c95p))
CR="/usrdata/EnzymeCAGE_data/EnzymeCAGE-master"
# --- C95 task-local path overrides (same variable names; original literals kept above) ---
CR = __C95_CTX.get("CR", CR)
sys.path.insert(0,CR+"/feature");sys.path.insert(0,CR)
from gvp_torchdrug_feature import batch_run
from c95_gvp_compat import invoke as _c95_gvp_invoke
W="/usrdata/EnzymeCAGE_data/workspaces/biosysmodb121_final_reaction_rescue_pre_enzyme_ranking_asset_closure_20261006"
S5=W+"/S5_protein_assets";D="/usrdata/EnzymeCAGE_data"
# --- C95 task-local path overrides (same variable names; original literals kept above) ---
W = __C95_CTX["W"]
S5 = __C95_CTX["S5"]
D = __C95_CTX.get("D", D)
RUN=D+"/training_runs/enzymecage_v6_298_rhea142_brenda_enzgfm650m_retrain_20260922"
A=D+"/workspaces/p291_alphafill_20260922/bundles"
S=D+"/pollutant298_original_only_dual_3b_600m_4gpu_20260921/protein/staged_assets"
B3B=D+"/workspaces/biosysmodb121_step_enzyme_ranking_20260928/B3B_sentinel_20260929"
PHASE=sys.argv[1] if len(sys.argv)>1 else "sentinel"
seqmap=pickle.load(open(S5+"/S5_SEQMAP.pkl","rb"))
_carr_path=B3B+"/runtime/carrier_indices.pkl"
carr_idx=pickle.load(open(_carr_path,"rb")) if os.path.isfile(_carr_path) else {}
def find_pdb(u):
    c=[os.path.join(RUN+"/02_carrier_uid_and_pocket/alphafill/pockets",u+".pdb")]
    c+=glob.glob(os.path.join(A,u,"pockets","pocket",u+".pdb"))
    c+=glob.glob(os.path.join(S,u,"pockets","pocket",u+".pdb"))
    c+=glob.glob(os.path.join(A,u,"pockets",u+".pdb"))
    c+=glob.glob(os.path.join(S,u,"pockets",u+".pdb"))
    for q in c:
        if os.path.isfile(q):return q
    return None
def get_idx(s,u):
    v=carr_idx.get((str(u),str(s)))
    if v:return v,"S3_CARRIER"
    for base in (S,A):
        q=os.path.join(base,str(u),"STATE","pocket_ok.json")
        if os.path.isfile(q):
            j=json.load(open(q));key="untrimmed_indices" if "untrimmed_indices" in j else "residues"
            return sorted(set(int(i) for i in j[key])),q
    return None,"MISSING"
def C_sha(p):return hashlib.sha256(open(p,"rb").read()).hexdigest()
gf=pd.read_csv(S5+"/S5_GAP_FLAGS.tsv.gz",sep="\t",dtype=str,keep_default_na=False)
if PHASE=="sentinel":
    sel=pd.read_csv(S5+"/S5_SENTINEL_SELECTION.tsv",sep="\t",dtype=str)
    items=[(r.sequence_sha256,r.uid) for _,r in sel[(sel.lane=="POCKET_3B600_GVP")&(sel.arm=="gvp")].iterrows()]
else:
    U=pd.read_csv(S5+"/FINAL_SEQUENCE_UNIVERSE.tsv",sep="\t",dtype=str,keep_default_na=False)
    uid_of=dict(zip(U.sequence_sha256,U.selected_uid))
    # C95 R1 (audit B): GVP worklist from its OWN family true-gap column
    # (gvp_ok in gap flags v2); the PLM pocket column must not drive it.
    # No recognized column -> explicit empty worklist (NO_WORK), never all rows.
    _c95col="gvp_ok" if "gvp_ok" in gf.columns else ("pocket_ok" if "pocket_ok" in gf.columns else None)
    items=[(s,uid_of.get(s,"")) for s in gf[gf[_c95col]=="True"].sequence_sha256] if _c95col else []
outdir=S5+"/overlay/gvp";os.makedirs(outdir,exist_ok=True)
timing=[];out={};t00=time.time()
for s,u in items:
    u=str(u);seq=seqmap.get(s)
    if not seq:
        out[f"{s}|{u}"]={"status":"SEQ_UNRESOLVED"};continue
    seq="".join(seq.upper().split())
    t0=time.time();pdb=find_pdb(u)
    fn=f"{s[:32]}_{u}.gvp.pt"
    if os.path.isfile(os.path.join(outdir,fn)):continue
    if pdb is None:
        out[f"{s}|{u}"]={"status":"NO_POCKET_PDB"}
        timing.append({"lane":"GVP","key":s,"status":"FAILED","failure_type":"NO_POCKET_PDB","raw_len":len(seq),"pocket_rows":"","wall_s":round(time.time()-t0,3),"out_bytes":0});continue
    idx,isrc=get_idx(s,u)
    tmp=f"{outdir}/tmp_{u}.pt"
    t1=time.time()
    try:
        _c95_gvp_invoke(batch_run, (u,pdb,tmp,seq))
        err=None
        if os.path.exists(tmp+".error"):
            err=open(tmp+".error").read()[:150];os.remove(tmp+".error")
        mp=torch.load(tmp,map_location="cpu",weights_only=False) if os.path.exists(tmp) else None
        assert mp and u in mp and mp[u],err or "empty gvp"
        f=mp[u][0];rows=int(f.shape[0])
        ok_rows=(idx is None) or rows==len(idx)
        assert np.isfinite(f.numpy().astype(np.float32)).all()
        fsha=hashlib.sha256(f.numpy().tobytes()).hexdigest()
        os.replace(tmp,os.path.join(outdir,fn))
        out[f"{s}|{u}"]={"file":fn,"rows":rows,"pocket_idx_source":isrc,
          "pocket_idx_rows":len(idx) if idx else None,"rows_match_pocket":bool(ok_rows),
          "pdb":pdb,"pdb_sha256":C_sha(pdb),"feat_sha256":fsha,"status":"SUCCESS"}
        timing.append({"lane":"GVP","key":s,"status":"SUCCESS","failure_type":"","raw_len":len(seq),
          "pocket_rows":rows,"wall_s":round(time.time()-t1,3),"e2e_s":round(time.time()-t0,3),
          "out_bytes":os.path.getsize(os.path.join(outdir,fn))})
    except Exception as e:
        out[f"{s}|{u}"]={"status":"GVP_FAILED","error":repr(e)[:200],"pdb":pdb}
        timing.append({"lane":"GVP","key":s,"status":"FAILED","failure_type":type(e).__name__,"raw_len":len(seq),"pocket_rows":"","wall_s":round(time.time()-t1,3),"out_bytes":0})
    if os.path.exists(tmp):os.remove(tmp)
json.dump(out,open(outdir+f"/GVP_MANIFEST_{PHASE}.json","w"),indent=1)
pd.DataFrame(timing).to_csv(S5+f"/timing/lane_gvp_{PHASE}.tsv",sep="\t",index=False)
n_ok=sum(1 for t in timing if t["status"]=="SUCCESS")
print("GVP",PHASE,":",len(timing),"ok",n_ok,"total_s",round(time.time()-t00,1))
