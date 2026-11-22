#!/usrdata/EnzymeCAGE_envs/enzymecage_py312/bin/python
"""B3B STRUCT8 lane: bounded real structure/pocket pipeline per frozen route.
1) exact-sequence historical re-check (S3/alphafill/staged pocket PDBs)
2) AlphaFill 8A frozen route: AUTH endpoints/naming {uid}_transplant.cif+.json
   (max 2 curl attempts per endpoint), then AUTH extract_alphafill_gap_pockets.py
   unchanged + Q4-style identity audit with entity_poly_seq mapping
3) only on explicit AlphaFill failure: AFDB download + P2Rank 2.5.1 fallback
Typed terminal statuses only; no UID substitution."""
import csv, hashlib, json, os, pickle, shutil, subprocess, sys, time
import numpy as np, pandas as pd
from Bio.PDB import PDBParser
# --- C95 task-local context loader (inserted; original code untouched) ---
import json as _c95json, os as _c95os
_c95p = _c95os.environ.get("C95_LANE_CONTEXT")
if not _c95p:
    raise SystemExit("C95_LANE_CONTEXT env (task-local path context JSON) required for C95 adapted copies")
__C95_CTX = _c95json.load(open(_c95p))

B="/usrdata/EnzymeCAGE_data/workspaces/biosysmodb121_pre_ranking_r1_reaction_protein_asset_gold_closure_20261008/R3_structure_protein/struct_lane"
# --- C95 task-local path overrides (same variable names; original literals kept above) ---
B = __C95_CTX["B"]
VOCAB={"POCKET_OK","ALPHAFILL_UNAVAILABLE","AFDB_UNAVAILABLE","SEQUENCE_MISMATCH",
       "CHAIN_MAPPING_AMBIGUOUS","NO_VALID_POCKET","P2RANK_FAILED","TOOL_UNAVAILABLE"}
def vocab_map(stt,detail):
    d=str(detail).upper()
    if stt=="SEQ_TEXT_UNRESOLVED":return "SEQUENCE_MISMATCH"
    if "IDENTITY_MISMATCH" in d or "ENTITY_AA_MISMATCH" in d or "SEQ_SHORT" in d:
        return "SEQUENCE_MISMATCH"
    if stt in("NO_VALID_POCKET","P2RANK_FAILED") and ("NOT_IN_ENTITY" in d or "NO_STD_RESIDUES" in d):
        return "CHAIN_MAPPING_AMBIGUOUS"
    return stt
D="/usrdata/EnzymeCAGE_data"
RUN=D+"/training_runs/enzymecage_v6_298_rhea142_brenda_enzgfm650m_retrain_20260922"
AW=D+"/workspaces/p291_alphafill_20260922/authwork/work/custom_data_build"
# --- C95 task-local path overrides (same variable names; original literals kept above) ---
D = __C95_CTX.get("D", D)
RUN = __C95_CTX.get("RUN", RUN)
AW = __C95_CTX.get("AW", AW)
EX=AW+"/extract_alphafill_gap_pockets.py"
P2R=D+"/tools/p2rank_2.5.1/prank"
PY=sys.executable
import os as _os
_os.makedirs(B,exist_ok=True)
SEQMAP_C95 = __C95_CTX.get("SEQMAP", "/usrdata/EnzymeCAGE_data/workspaces/biosysmodb121_final_reaction_rescue_pre_enzyme_ranking_asset_closure_20261006/S5_protein_assets/S5_SEQMAP.pkl")
# C95 R1 (audit B): SEQMAP is a task-context field and MUST point at the
# CURRENT gen/s5/S5_SEQMAP.pkl (21,637 sequences incl. newly added ones); the
# 2026-10-06 literal survives only as the documented fallback default.
seqmap=pickle.load(open(SEQMAP_C95,"rb"))
# full deployment: deterministic shard from STRUCT_FULL_WORKLIST (argv[1]);
# resumable within TASK_ID; completed shards immutable via SHARD_DONE.json.
SHARD=sys.argv[1]
SDIR=B+"/full/shard_"+SHARD
if os.path.isfile(SDIR+"/SHARD_DONE.json"):
    print("shard",SHARD,"DONE (immutable) - skip");sys.exit(0)
os.makedirs(SDIR,exist_ok=True)
WL=pd.read_csv(B+"/full/R3_STRUCTURE_WORKLIST.tsv",sep="\t",dtype=str,keep_default_na=False)
S8=WL[WL.shard_id==SHARD][["work_item_id","sequence_sha256","selected_uid","raw_length"]].copy()
prev={}
if os.path.isfile(SDIR+"/STATUS.tsv"):
    for r in pd.read_csv(SDIR+"/STATUS.tsv",sep="\t",dtype=str,keep_default_na=False).itertuples():
        prev[r.sequence_sha256]=r._asdict()
_rows=[]
for _,rr in S8.iterrows():
    if rr.sequence_sha256 in prev:
        src=dict(prev[rr.sequence_sha256]);src["work_item_id"]=rr.work_item_id
        src["detail"]=(str(src.get("detail",""))+"|resumed_attempt").strip("|")
        _rows.append(src)
S8=S8[~S8.sequence_sha256.isin({r["sequence_sha256"] for r in _rows})]
from Bio.Data.IUPACData import protein_letters_3to1 as T31
THREE2ONE={three.upper():one.upper() for three,one in T31.items()}
ONE2THREE={one.upper():three.upper() for three,one in T31.items()}
STD=set(THREE2ONE)

def hist_recheck(u):
    for p in [RUN+"/02_carrier_uid_and_pocket/alphafill/pockets/"+u+".pdb",
              D+f"/workspaces/p291_alphafill_20260922/bundles/{u}/pockets/pocket/{u}.pdb",
              D+f"/pollutant298_original_only_dual_3b_600m_4gpu_20260921/protein/staged_assets/{u}/pockets/pocket/{u}.pdb"]:
        if os.path.isfile(p) and os.path.getsize(p)>0:
            return p
    return None

def entity_poly_resnums(cif_path):
    try:
        ls=open(cif_path,errors="ignore").read().splitlines()
    except Exception:
        return None
    start=None
    for i,l in enumerate(ls):
        if l.startswith("_entity_poly_seq."): start=i; break
    if start is None: return None
    hdr=ls[start].split()
    if "num" not in hdr or "mon_id" not in hdr: return None
    ni=hdr.index("num"); mi=hdr.index("mon_id"); pairs=[]
    for l in ls[start+1:]:
        if not l.strip() or l.startswith(("#","_","loop_","stop_")): break
        parts=l.split()
        try: pairs.append((int(parts[ni]), parts[mi].upper().strip("'\"")))
        except Exception: break
    return pairs or None

def audit_pocket(u, pdbf, seq, cif=None):
    try:
        parser=PDBParser(QUIET=True)
        st=parser.get_structure("x", pdbf)
        ch=next(iter(st[0].get_chains()))
    except Exception as e:
        return None, "PDB_PARSE:"+type(e).__name__
    res=[r for r in ch if r.get_resname().upper() in STD and r.id[0]==" "]
    pos=aa_by=None
    if cif and os.path.isfile(cif):
        pairs=entity_poly_resnums(cif)
        if pairs:
            pos={num:i for i,(num,mid) in enumerate(pairs)}
            aa_by=dict(pairs)
    idxs=[]
    for r in res:
        num=r.id[1]
        if pos is None:
            sp=num-1
        else:
            if num not in pos: return None,f"RES{num}_NOT_IN_ENTITY"
            sp=pos[num]
            if aa_by.get(num) and aa_by[num]!=THREE2ONE.get(r.get_resname().upper()):
                return None,f"ENTITY_AA_MISMATCH@{num}"
        if sp>=len(seq): return None,"SEQ_SHORT"
        if THREE2ONE.get(r.get_resname().upper())!=seq[sp]:
            return None,f"IDENTITY_MISMATCH@{num}"
        idxs.append(sp+1)
    if not idxs: return None,"NO_STD_RESIDUES"
    if min(idxs)<1 or max(idxs)>len(seq): return None,"IDX_RANGE"
    return sorted(set(idxs)), "OK"

def curl_pair(urls):
    codes=[]
    for tgt,url in urls:
        code=""
        ok=False
        for _ in range(2):
            try:
                q=subprocess.run(["curl","-s","-S","-L","--connect-timeout","15","--max-time","90",
                                  "-w","%{http_code}","-o",tgt,url],capture_output=True,text=True,timeout=120)
                code=q.stdout.strip()[-3:] if q.stdout else str(q.returncode)
            except (subprocess.TimeoutExpired,OSError) as e:
                code="CURL_"+type(e).__name__
            codes.append(code)
            ok = code=="200" and os.path.isfile(tgt) and os.path.getsize(tgt)>0
            if ok: break
        if not ok and os.path.isfile(tgt):
            os.remove(tgt)
        if not ok:
            return codes, False
    return codes, True

os.makedirs(B+"/structure",exist_ok=True)
rows=_rows
for r in S8.itertuples():
    s=str(r.sequence_sha256); u=str(r.selected_uid)
    if s not in seqmap:
        rows.append({"work_item_id":str(r.work_item_id),"uid":u,"sequence_sha256":s,"route":"",
          "status":"SEQUENCE_MISMATCH","http":"","seconds":0,"retries":0,"pdb":"","pocket_pdb":"",
          "pocket_rows":"","pocket_idx_file":"","detail":"SEQ_TEXT_UNRESOLVED: no resolved sequence text (416-family typed gap); identity audit impossible without exact sequence"})
        continue
    seq="".join(str(seqmap[s]).upper().split())
    work=os.path.join(B,"work/struct",u); os.makedirs(work,exist_ok=True)
    raw=os.path.join(work,"raw"); os.makedirs(raw,exist_ok=True)
    st={"work_item_id":str(r.work_item_id),"uid":u,"sequence_sha256":s,"route":"","status":"","http":"","seconds":0,
        "retries":0,"pdb":"","pocket_pdb":"","pocket_rows":"","pocket_idx_file":"","detail":""}
    t0=time.time()
    hp=hist_recheck(u)
    if hp:
        pdbf=os.path.join(work,f"{u}_hist.pdb"); shutil.copyfile(hp,pdbf)
        idx,why=audit_pocket(u,pdbf,seq)
        if idx:
            st.update(route="historical_recheck",status="POCKET_OK",pdb=hp,pocket_pdb=pdbf,
                      pocket_rows=len(idx),pocket_idx_file=os.path.join(work,"pocket_ok_hist.json"),
                      detail=hashlib.sha256(open(pdbf,'rb').read()).hexdigest())
            json.dump({"uid":u,"untrimmed_indices":idx,"source":"HISTORICAL_RECHECK"},
                      open(work+"/pocket_ok_hist.json","w"))
            st["seconds"]=round(time.time()-t0,1); rows.append(st); continue
        st["detail"]="HIST_PDB_AUDIT_FAIL:"+why
    cif=os.path.join(raw,f"{u}_transplant.cif"); js=os.path.join(raw,f"{u}_transplant.json")
    codes,ok_dl=curl_pair([(cif,f"https://alphafill.eu/v1/aff/{u}"),
                           (js,f"https://alphafill.eu/v1/aff/{u}/json")])
    st["http"]=",".join(codes); st["retries"]=max(0,len(codes)-2)
    if ok_dl:
        okm=os.path.join(work,"success.csv")
        pd.DataFrame([{"UniprotID":u}]).to_csv(okm,index=False)
        pw=os.path.join(work,"pocketw")
        try:
            subprocess.run([PY,EX,"--success_manifest",okm,"--raw_download_dir",raw,
                "--pocket_dir",os.path.join(pw,"pocket"),
                "--pocket_info_csv",os.path.join(pw,"pocket_info.csv"),
                "--n_process","1"],capture_output=True,text=True,timeout=600)
        except (subprocess.TimeoutExpired,OSError) as e:
            st["detail"]=(st["detail"]+" EXTRACT_"+type(e).__name__).strip()
        pdbf=os.path.join(pw,"pocket",u+".pdb")
        if os.path.isfile(pdbf):
            idx,why=audit_pocket(u,pdbf,seq,cif=cif)
            if idx:
                st.update(route="alphafill_8a",status="POCKET_OK",pdb=cif,pocket_pdb=pdbf,
                          pocket_rows=len(idx),pocket_idx_file=os.path.join(work,"pocket_ok.json"),
                          detail=hashlib.sha256(open(pdbf,'rb').read()).hexdigest())
                json.dump({"uid":u,"untrimmed_indices":idx,"source":"ALPHAFILL_8A"},
                          open(work+"/pocket_ok.json","w"))
                st["seconds"]=round(time.time()-t0,1); rows.append(st); continue
            st["detail"]="AF_POCKET_AUDIT_FAIL:"+why
            st.update(route="alphafill_8a",status="NO_VALID_POCKET",pdb=cif)
        else:
            st.update(route="alphafill_8a",status="NO_VALID_POCKET",pdb=cif,detail="no pocket pdb")
    else:
        st.update(route="alphafill",status="ALPHAFILL_UNAVAILABLE",detail="download failed "+st["http"])
    if st["status"] in ("ALPHAFILL_UNAVAILABLE","NO_VALID_POCKET"):
        af=None; url=""
        for v in ("v6","v5","v4"):
            url=f"https://alphafold.ebi.ac.uk/files/AF-{u}-F1-model_{v}.pdb"
            try:
                q=subprocess.run(["curl","-s","-S","-L","--retry","2","--connect-timeout","15",
                                  "--max-time","120","-o",os.path.join(work,f"af_{u}.pdb"),url],
                                 capture_output=True,text=True,timeout=180)
                qrc=q.returncode
            except (subprocess.TimeoutExpired,OSError):
                qrc=-1
            pth=os.path.join(work,f"af_{u}.pdb")
            if qrc==0 and os.path.isfile(pth) and os.path.getsize(pth)>1000:
                af=url; break
            if os.path.isfile(pth): os.remove(pth)
        if af is None:
            st.update(route=st["route"]+"->afdb",status="AFDB_UNAVAILABLE",
                      detail=(st["detail"]+" | afdb 404 v6/v5/v4").strip(" |"))
            st["seconds"]=round(time.time()-t0,1); rows.append(st); continue
        pr=os.path.join(work,"p2rank_out"); os.makedirs(pr,exist_ok=True)
        try:
            p3=subprocess.run([P2R,"predict","-f",os.path.join(work,f"af_{u}.pdb"),
                "-o",pr],capture_output=True,text=True,timeout=900)
        except Exception as e:
            p3=None; st["detail"]="P2RANK_TIMEOUT:"+str(e)[:80]
        best=None
        predcsv=os.path.join(pr,f"af_{u}.pdb_predictions.csv")
        if os.path.isfile(predcsv):
            import csv as _csv
            rd=list(_csv.reader(open(predcsv)))
            if len(rd)>1:
                hdr=[h.strip() for h in rd[0]]
                ri=hdr.index("residue_ids")
                ranki=hdr.index("rank")
                row=min(rd[1:], key=lambda r: int(r[ranki].strip()))
                resnums=[int(t.split("_")[1]) for t in row[ri].split() if "_" in t]
                # write pocket PDB from AFDB atoms of those residues
                src=os.path.join(work,f"af_{u}.pdb")
                keep=[]
                for l in open(src):
                    if l.startswith("ATOM"):
                        num=int(l[22:26])
                        if num in resnums: keep.append(l)
                    elif l.startswith(("TER","END")): continue
                best=os.path.join(work,f"{u}_p2rank_cluster.pdb")
                with open(best,"w") as h:
                    h.writelines(keep); h.write("TER\nEND\n")
        if best:
            idx,why=audit_pocket(u,best,seq)
            if idx:
                dst=os.path.join(work,f"{u}_p2rank.pdb"); shutil.copyfile(best,dst)
                st.update(route=st["route"]+"->afdb_p2rank",status="POCKET_OK",pdb=af,
                          pocket_pdb=dst,pocket_rows=len(idx),
                          pocket_idx_file=os.path.join(work,"pocket_ok.json"),
                          detail=hashlib.sha256(open(dst,'rb').read()).hexdigest())
                json.dump({"uid":u,"untrimmed_indices":idx,"source":"P2Rank_2.5.1",
                           "afdb_url":af}, open(work+"/pocket_ok.json","w"))
                st["seconds"]=round(time.time()-t0,1); rows.append(st); continue
            st["detail"]=(st["detail"]+" P2RANK_AUDIT_FAIL:"+why).strip()
        if not str(st["status"]).endswith("POCKET_OK"):
            st.update(route=st["route"]+"->afdb_p2rank",status="P2RANK_FAILED",pdb=af)
    st["seconds"]=round(time.time()-t0,1)
    rows.append(st)

df=pd.DataFrame(rows)
# final terminal vocabulary (contract §7.2): no PENDING_RESUME / NOT_RUN / empty
df["status"]=[vocab_map(s,d) for s,d in zip(df.status,df.detail)]
assert set(df.status)<=VOCAB, f"non-vocab statuses: {set(df.status)-VOCAB}"
assert (df.status!="").all()
cols=["work_item_id","uid","sequence_sha256","route","status","http","seconds",
      "retries","pdb","pocket_pdb","pocket_rows","pocket_idx_file","detail"]
for c in cols:
    if c not in df.columns:df[c]=""
df=df[cols].sort_values("work_item_id")
df.to_csv(SDIR+"/STATUS.tsv",sep="\t",index=False)
h=hashlib.sha256(open(SDIR+"/STATUS.tsv","rb").read()).hexdigest()
json.dump({"shard":SHARD,"items":len(df),"status_tsv_sha256":h,
           "counts":df.status.value_counts().to_dict(),
           "utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())},
          open(SDIR+"/SHARD_DONE.json","w"),indent=1)
print("shard",SHARD,"done:",json.dumps(df.status.value_counts().to_dict()))
