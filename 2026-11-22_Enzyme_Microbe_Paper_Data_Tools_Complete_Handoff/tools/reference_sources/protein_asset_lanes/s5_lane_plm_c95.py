#!/usr/data/EnzymeCAGE_envs/esm_extraction_py312/bin/python
"""S5 §10.2-10.3 PLM lane (legacy arms). Frozen science (B3B-audited contracts):
3B: esm2_t36_3B fair-esm layer-36 representations (L+2,2560); global=mean(0);
    pocket=node[biological 1-based indices] float32.
600M legacy: ESMC logits embeddings[0] (L+2,1152); global=mean(0); pocket=node[idx].
Phases: pc (native positive control vs frozen base store, max-abs-delta gate 2e-4,
NOT loosened), sentinel, full. One GPU worker, batch=1. All output task-local overlay."""
import argparse,hashlib,json,os,pickle,subprocess,sys,time
import numpy as np,pandas as pd,torch
# --- C95 task-local context loader (inserted; original code untouched) ---
import json as _c95json, os as _c95os
_c95p = _c95os.environ.get("C95_LANE_CONTEXT")
if not _c95p:
    raise SystemExit("C95_LANE_CONTEXT env (task-local path context JSON) required for C95 adapted copies")
__C95_CTX = _c95json.load(open(_c95p))
W="/usrdata/EnzymeCAGE_data/workspaces/biosysmodb121_final_reaction_rescue_pre_enzyme_ranking_asset_closure_20261006"
S5=W+"/S5_protein_assets";D="/usrdata/EnzymeCAGE_data"
# --- C95 task-local path overrides (same variable names; original literals kept above) ---
W = __C95_CTX["W"]
S5 = __C95_CTX["S5"]
D = __C95_CTX.get("D", D)
CKPT3B="/root/.cache/torch/hub/checkpoints/esm2_t36_3B_UR50D.pt"
# --- C95 task-local path overrides (same variable names; original literals kept above) ---
CKPT3B = __C95_CTX.get("CKPT3B", CKPT3B)
LEG600=D+"/models/esmc_600m"
ap=argparse.ArgumentParser()
ap.add_argument("--arm",required=True,choices=["legacy_esm2_3b","legacy_esmc600m"])
ap.add_argument("--phase",required=True,choices=["pc","sentinel","full","full2"])
# full2 = disclosed catch-up attempt: identical frozen science, but the GLOBAL
# worklist is re-derived from the final seqmap (the EBI fetch resolved 1,312
# more sequences AFTER S5_GAP_FLAGS was frozen); items remain a subset of the
# frozen FINAL_ASSET_WORK_ITEMS list; existing overlay files are skipped.
ap.add_argument("--max-delta",type=float,default=2e-4)
A=ap.parse_args()
os.environ.setdefault("CUDA_VISIBLE_DEVICES","0")
seqmap=pickle.load(open(S5+"/S5_SEQMAP.pkl","rb"))
sel=pd.read_csv(S5+"/S5_SENTINEL_SELECTION.tsv",sep="\t",dtype=str)
gapfl=pd.read_csv(S5+"/S5_GAP_FLAGS.tsv.gz",sep="\t",dtype=str,keep_default_na=False)
U=pd.read_csv(S5+"/FINAL_SEQUENCE_UNIVERSE.tsv",sep="\t",dtype=str,keep_default_na=False)
uid_of=dict(zip(U.sequence_sha256,U.selected_uid))
carr_idx=pickle.load(open(D+"/workspaces/biosysmodb121_step_enzyme_ranking_20260928/B3B_sentinel_20260929/runtime/carrier_indices.pkl","rb"))
oldpock=pickle.load(open(D+"/feature/protein/ESM2_3B_corrected_107705/metadata/final_corrected_pocket_indices.pkl","rb"))
POK=[D+"/pollutant298_original_only_dual_3b_600m_4gpu_20260921/protein/staged_assets",
     D+"/workspaces/p291_alphafill_20260922/bundles"]
def get_pocket(s,u):
    v=carr_idx.get((str(u),str(s)))
    if v:return v,"S3_CARRIER"
    for b in POK:
        q=os.path.join(b,str(u),"STATE","pocket_ok.json")
        if os.path.isfile(q):
            j=json.load(open(q));key="untrimmed_indices" if "untrimmed_indices" in j else "residues"
            ii=sorted(set(int(i) for i in j[key]))
            if ii:return ii,q
    v=oldpock.get(u)
    if v is not None:return sorted(set(int(i) for i in (v if hasattr(v,"__iter__") else [v]))),"OLD_POCKET_INDEX"
    return None,"MISSING"
dim=2560 if A.arm=="legacy_esm2_3b" else 1152
if A.arm=="legacy_esm2_3b":
    GSTORE=D+"/feature/protein/ESM2_3B_corrected_107705/protein_level/seq2feature.pkl"
    PSTORE=D+"/feature/protein/ESM2_3B_corrected_107705/pocket_node_feature/esm_node_feature.torch.pt"
else:
    GSTORE=D+"/feature/protein/ESM-C_600M_baseline_1152_round1_20260708/protein_level/seq2feature.pkl"
    PSTORE=D+"/feature/protein/ESM-C_600M_baseline_1152_round1_20260708/pocket_node_feature/esm_node_feature.torch.pt"
gstore=pickle.load(open(GSTORE,"rb"))
import zipfile as _zf
try:
    pstore=(torch.load(PSTORE,map_location="cpu",mmap=True,weights_only=False)
            if _zf.is_zipfile(PSTORE) else torch.load(PSTORE,map_location="cpu",weights_only=False))
except Exception:
    pstore=pickle.load(open(PSTORE,"rb"))
def canon(t):return "".join(str(t).upper().split())
_t=time.time()
if A.arm=="legacy_esm2_3b":
    import esm.pretrained as ep
    import argparse as _ap
    torch.serialization.add_safe_globals([_ap.Namespace])
    _orig=torch.load
    try:_m,_alpha=ep.load_model_and_alphabet_local(CKPT3B)
    finally:torch.load=_orig
    _m=_m.to("cuda").eval();_bc=_alpha.get_batch_converter()
    def fwd(seq):
        with torch.no_grad():
            _,_,tok=_bc([("u",seq)])
            o=_m(tok.to("cuda"),repr_layers=[36])
        return o["representations"][36][0].detach().cpu().float().numpy()
else:
    os.environ["TRANSFORMERS_OFFLINE"]="1";os.environ["HF_HOME"]=LEG600
    sys.path.insert(0,os.path.join(LEG600,"hub"))
    from esm.models.esmc import ESMC
    from esm.sdk.api import ESMProtein,LogitsConfig
    _e=ESMC.from_pretrained("esmc_600m").to("cuda").eval()
    def fwd(seq):
        with torch.no_grad():
            lo=_e.logits(_e.encode(ESMProtein(sequence=seq)),LogitsConfig(sequence=True,return_embeddings=True))
        return lo.embeddings[0].detach().cpu().float().numpy()
COLD=time.time()-_t
os.makedirs(S5+f"/overlay/global/{A.arm}",exist_ok=True)
os.makedirs(S5+f"/overlay/pocket/{A.arm}",exist_ok=True)
os.makedirs(S5+"/timing",exist_ok=True)
TIM=S5+"/timing/lane_"+A.arm+".tsv"
def trec(lane,key,status,ft,L,rows,warm,post,peak,out_b):
    new=not os.path.isfile(TIM)
    with open(TIM,"a") as f:
        if new:f.write("lane\tarm\tkey\tstatus\tfailure_type\traw_len\tpocket_rows\twarm_forward_s\tpost_write_s\tpeak_alloc_MiB\tpeak_reserved_MiB\tout_bytes\tcold_load_s\n")
        f.write(f"{lane}\t{A.arm}\t{key}\t{status}\t{ft}\t{L}\t{rows}\t{round(warm,4)}\t{round(post,4)}\t{round(peak[0]/2**20,1)}\t{round(peak[1]/2**20,1)}\t{out_b}\t{round(COLD,3)}\n")
def pk():return (torch.cuda.max_memory_allocated(),torch.cuda.max_memory_reserved())
def pc():
    """B3B-frozen native positive control: iterate pocket store UIDs, find the
    sequence via the 3B uid manifest, fresh forward, compare stored global+pocket."""
    ou=pd.read_csv(D+"/feature/protein/ESM2_3B_corrected_107705/metadata/final_uid_sequence_manifest.csv",dtype=str,keep_default_na=False)
    seqc=[c for c in ou.columns if "seq" in c.lower()][0];uidc=ou.columns[0]
    oumap=dict(zip(ou[uidc].astype(str),ou[seqc]))
    pc_key=None;dg=dp=None;status="FAIL"
    for uid,pnode in pstore.items():
        uid=str(uid);seq=oumap.get(uid)
        if seq is None or len(seq)<40 or len(seq)>700:continue
        pc_key=uid
        torch.cuda.reset_peak_memory_stats()
        t0=time.time();node=fwd(canon(seq));warm=time.time()-t0
        g=node.mean(axis=0).astype(np.float32)
        base_g=np.asarray(gstore[seq if seq in gstore else canon(seq)],dtype=np.float32) if (seq in gstore or canon(seq) in gstore) else None
        dg=float(np.max(np.abs(base_g-g))) if base_g is not None else None
        idx=oldpock.get(uid)
        base_p=np.asarray(pnode,dtype=np.float32)
        if idx is not None and base_p.shape[0]==len(idx):
            poc=node[np.asarray(idx,dtype=int)].astype(np.float32)
            dp=float(np.max(np.abs(base_p-poc)))
        else:dp=None
        ok=(dg is not None and dg<=A.max_delta and dp is not None and dp<=A.max_delta)
        status="PASS" if ok else f"FAIL(global_d={dg},pocket_d={dp})"
        trec("POSITIVE_CONTROL",uid,"POS_"+status,"",len(seq),len(idx) if idx else 0,warm,0,pk(),0)
        break
    json.dump({"arm":A.arm,"control_uid":pc_key,"cold_load_s":round(COLD,2),
      "max_delta_gate":A.max_delta,"global_max_abs_delta":dg,"pocket_max_abs_delta":dp,
      "status":status,"utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())},
      open(S5+f"/PC_{A.arm}.json","w"),indent=1)
    if status!="PASS":
        json.dump({"arm":A.arm,"status":"BLOCKED_CONTRACT_REPLAY_FAILED","detail":status,"control":pc_key,
          "consequence":"entire legacy 600M lane NO_GO; 15,295 typed work items preserved; tolerance NOT loosened" if A.arm=="legacy_esmc600m" else "3B lane blocked"},
          open(S5+f"/BLOCKED_{A.arm}.json","w"),indent=1)
    print("PC:",status)
    return status=="PASS"
if A.phase=="pc":
    ok=pc();print("PC","PASS" if ok else "FAIL");sys.exit(0 if ok else 3)
pcj=S5+f"/PC_{A.arm}.json"
if not os.path.isfile(pcj) or json.load(open(pcj))["status"]!="PASS":
    print("BLOCKED: positive control not passed for this arm; lane NO_GO");sys.exit(4)
if A.phase=="sentinel":
    items=sel[(sel.lane=="GLOBAL")&(sel.arm==A.arm)]
    pitems=sel[(sel.lane=="POCKET_3B600_GVP")&(sel.arm==A.arm)]
else:
    if A.phase=="full2":
        # C95 R1.1 (audit §5.2 zero-gap first run): the historical list-comprehension
        # df[[...]] selects LABELS when the mask is empty, producing a 0-column frame
        # and crashing the very next line on truly-empty gaps. Row-mask form is
        # equivalent whenever rows exist; selection semantics unchanged.
        g=gapfl[gapfl.sequence_sha256.isin(list(seqmap))]
        # C95 R1 (audit B): true-gap filter AT THE OLD SELECTION SITE. Gap flags
        # v2 (make_reuse_inputs --from-union) carries per-family columns from the
        # union inventory; rows already covered by formal/old overlays must never
        # re-forward. Fail-closed: an old-schema file without global_gap would
        # select EVERYTHING (the exact audit-B defect), so it is refused.
        # Embedding math and output recipe untouched.
        if "global_gap" not in gapfl:
            raise SystemExit("GAP_FLAGS_SCHEMA_V2_REQUIRED: full2 needs the global_gap column "
                             "(regenerate via make_reuse_inputs --from-union)")
        g=g[g.global_gap=="True"]
    else:
        g=gapfl[gapfl.seq_ok=="True"] if "seq_ok" in gapfl else gapfl
    items=pd.DataFrame({"sequence_sha256":list(g.sequence_sha256),"uid":[uid_of.get(s,"") for s in g.sequence_sha256],"lane":"GLOBAL","arm":A.arm})
    p=gapfl[gapfl.pocket_ok=="True"] if "pocket_ok" in gapfl else gapfl.iloc[:0]
    pitems=pd.DataFrame({"sequence_sha256":list(p.sequence_sha256),"uid":[uid_of.get(s,"") for s in p.sequence_sha256],"lane":"POCKET","arm":A.arm})
n=0
for _,r in items.iterrows():
    s=r.sequence_sha256;seq=seqmap.get(s)
    o=S5+f"/overlay/global/{A.arm}/{s}.npy"
    if not seq:
        trec(A.phase+"_GLOBAL",s,"SKIP","SEQ_UNRESOLVED",0,0,0,0,pk(),0);continue
    if os.path.isfile(o):n+=1;continue
    t0=time.time();node=fwd(canon(seq));warm=time.time()-t0
    gv=node.mean(0).astype(np.float32)
    t1=time.time();np.save(o,gv);post=time.time()-t1
    trec(A.phase+"_GLOBAL",s,"SUCCESS","",len(seq),0,warm,post,pk(),os.path.getsize(o))
    n+=1
    if n%500==0:print("global",n,flush=True)
m=0
for _,r in pitems.iterrows():
    s=r.sequence_sha256;u=str(r.uid) if str(r.uid)!="nan" else uid_of.get(s,"")
    seq=seqmap.get(s)
    o=S5+f"/overlay/pocket/{A.arm}/{s}__{u}.npy"
    if not seq:
        trec(A.phase+"_POCKET",s,"SKIP","SEQ_UNRESOLVED",0,0,0,0,pk(),0);continue
    idx,src=get_pocket(s,u)
    if not idx:
        trec(A.phase+"_POCKET",s,"SKIP","POCKET_INDEX_MISSING",len(seq),0,0,0,pk(),0);continue
    if os.path.isfile(o):m+=1;continue
    t0=time.time();node=fwd(canon(seq));warm=time.time()-t0
    if max(idx)>node.shape[0]-2:
        trec(A.phase+"_POCKET",s,"SKIP","INDEX_OUT_OF_RANGE",len(seq),0,warm,0,pk(),0);continue
    pv=node[[i for i in idx]].astype(np.float32)
    t1=time.time();np.save(o,pv);post=time.time()-t1
    trec(A.phase+"_POCKET",s,"SUCCESS",src,len(seq),len(idx),warm,post,pk(),os.path.getsize(o))
    m+=1
    if m%300==0:print("pocket",m,flush=True)
print("DONE global",n,"pocket",m)
