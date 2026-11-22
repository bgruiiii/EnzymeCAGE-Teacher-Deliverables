"""
TASK-LOCAL VERBATIM COPY of the frozen Chenyu baseline algorithm.
Sources (read-only, identity-checked at build time):
  /root/projects/EnzymeCAGE-master/retrieve.py
      sha256=67f3a475fcc88507b65c04cb45efe3522197c9bf22444b29d7ee9ae933d44fee
  /root/projects/EnzymeCAGE-master/utils.py  (get_rdkit_mol)
  /root/projects/EnzymeCAGE-master/enzymecage/base.py (UID_COL, RXN_COL, SEQ_COL)
  /root/projects/EnzymeCAGE-master/scripts/rhea_data_cleaning.py
      (canonicalization / cleaning chain used to build the old rhea_rxn2uids)
No logic may be changed here. s1b_equivalence.py proves this copy scores and
ranks identically to the originals on >=20 fixed reactions (abs err <= 1e-12).
"""
import math
from copy import deepcopy
from collections import defaultdict, Counter

import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import RDLogger
from rdkit.Chem import DataStructs

RDLogger.logger().setLevel(RDLogger.ERROR)

# --- from utils.py / enzymecage.base.py (verbatim) ---
def get_rdkit_mol(mol):
    if isinstance(mol, str):
        mol = Chem.MolFromSmiles(mol)
    return mol

UID_COL = 'UniprotID'
SEQ_COL = 'sequence'
RXN_COL = 'CANO_RXN_SMILES'

# --- from scripts/rhea_data_cleaning.py (verbatim) ---
def cano_smiles(smiles, remain_isomer=True):
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return None
    return Chem.MolToSmiles(mol, isomericSmiles=remain_isomer)

def calc_similarity(mol1, mol2):
    mol1 = get_rdkit_mol(mol1)
    mol2 = get_rdkit_mol(mol2)
    fp1 = AllChem.GetMorganFingerprint(mol1, 2)
    fp2 = AllChem.GetMorganFingerprint(mol2, 2)
    similarity = DataStructs.TanimotoSimilarity(fp1, fp2)
    return similarity

def remove_duplicate_mols(mols1, mols2):
    tmp1 = deepcopy(mols1)
    for mol1 in tmp1:
        flag = False
        for mol2 in mols2:
            simi = calc_similarity(mol1, mol2)
            if simi == 1:
                flag = True
                break
        if flag:
            mols1.remove(mol1)
            mols2.remove(mol2)
    return mols1, mols2

def neutralize_atoms(smi):
    try:
        mol = get_rdkit_mol(smi)
        pattern = Chem.MolFromSmarts("[+1!h0!$([*]~[-1,-2,-3,-4]),-1!$([*]~[+1,+2,+3,+4])]")
        at_matches = mol.GetSubstructMatches(pattern)
        at_matches_list = [y[0] for y in at_matches]
        if len(at_matches_list) > 0:
            for at_idx in at_matches_list:
                atom = mol.GetAtomWithIdx(at_idx)
                chg = atom.GetFormalCharge()
                hcount = atom.GetTotalNumHs()
                atom.SetFormalCharge(0)
                atom.SetNumExplicitHs(hcount - chg)
                atom.UpdatePropertyCache()

        smi_uncharged = Chem.MolToSmiles(mol)
        if not get_rdkit_mol(smi_uncharged):
            smi_uncharged = smi
    except Exception as e:
        print(e)
        print(f'Cannot neutralize SMILES: {smi}, use original format')
        smi_uncharged = smi

    return smi_uncharged

def neutralize_rxn(rxn):
    if not rxn:
        return None

    rcts = [neutralize_atoms(smi) for smi in rxn.split('>>')[0].split('.')]
    prods = [neutralize_atoms(smi) for smi in rxn.split('>>')[1].split('.')]

    return '.'.join(rcts) + '>>' + '.'.join(prods)

def remove_redundent_from_rxn(rxn, items_to_remove=None):
    if not rxn:
        return None

    # 金属和卤素离子这些先保留
    if not items_to_remove:
        items_to_remove = ['*', '[H+]', '[H]*[H]']

    rcts = [smi for smi in rxn.split('>>')[0].split('.') if smi not in items_to_remove]
    prods = [smi for smi in rxn.split('>>')[1].split('.') if smi not in items_to_remove]

    rcts, prods = remove_duplicate_mols(rcts, prods)

    if not rcts or not prods:
        return None

    return '.'.join(rcts) + '>>' + '.'.join(prods)

def count_carbon_atoms(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return 0
    return sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')

def filter_unwanted_rxn(rxn):
    if not rxn:
        return None

    rct = rxn.split('>>')[0]
    prod = rxn.split('>>')[1]

    rct_mol = get_rdkit_mol(rct)
    prod_mol = get_rdkit_mol(prod)

    if len(rct_mol.GetAtoms()) > 150 or len(prod_mol.GetAtoms()) > 150:
        return None

    rcts = rct.split('.')
    pros = prod.split('.')

    n_rct_w_carbon = sum([1 for rct in rcts if count_carbon_atoms(rct) > 0])
    n_prod_w_carbon = sum([1 for pro in pros if count_carbon_atoms(pro) > 0])

    if n_rct_w_carbon > 3 or n_prod_w_carbon > 3:
        return None
    elif n_rct_w_carbon == 0 or n_prod_w_carbon == 0:
        return None
    else:
        return rxn

def cano_rxn(rxn, exchange_pos=False, remain_isomer=True):
    if not rxn:
        return None
    data = rxn.split('>')
    reactants = data[0].split('.')
    reactants = [cano_smiles(each, remain_isomer) for each in reactants]
    products = data[-1].split('.')
    products = [cano_smiles(each, remain_isomer) for each in products]
    reactants = sorted(reactants)
    products = sorted(products)

    if not products or not reactants:
        return None

    if exchange_pos:
        new_rxn = f"{'.'.join(products)}>>{'.'.join(reactants)}"
    else:
        new_rxn = f"{'.'.join(reactants)}>>{'.'.join(products)}"
    return new_rxn

# --- from retrieve.py (verbatim) ---
def init_mapping_info(df_pos_pairs):
    if 'Label' in df_pos_pairs.columns:
        df_pos_pairs = df_pos_pairs[df_pos_pairs['Label'] == 1]

    uid_col = UID_COL if UID_COL in df_pos_pairs.columns else 'uniprotID'

    uid_to_seq = {}
    rxn_to_uid = defaultdict(set)
    for rxn, uid, seq in df_pos_pairs[[RXN_COL, uid_col, SEQ_COL]].values:
        uid_to_seq[uid] = seq
        rxn_to_uid[rxn].add(uid)

    return uid_to_seq, rxn_to_uid

def getRSim(rcts_smi_counter, pros_smi_counter, cand_rcts_molid_counter, cand_pros_molid_counter, sim):
    info_dict = {'s1': rcts_smi_counter, 'p1': pros_smi_counter, 's2': cand_rcts_molid_counter, 'p2':cand_pros_molid_counter}
    ss = {}
    simm = {}
    pairs = [('s1','s2'), ('s1', 'p2'), ('p1', 's2'), ('p1', 'p2')]
    compPairs = {}
    for pair_tuple in pairs:
        pairings = set()
        simm[pair_tuple] = {}
        compPairs[pair_tuple]=[]

        for mol_x in info_dict[pair_tuple[0]].keys():
            simm[pair_tuple][mol_x] = (0.0, mol_x, None)
            if mol_x in sim:
                for mol_y in info_dict[pair_tuple[1]].keys():
                    if mol_y in sim[mol_x]:
                        pairings.add( (sim[mol_x][mol_y], mol_x, mol_y) )

        found = {'left': set(), 'right': set()}
        for v in sorted(pairings, key = lambda h: -h[0]):
            if v[1] not in found['left'] and v[2] not in found['right']:
                # if similarity is greater that zero
                if v[0] > simm[pair_tuple][v[1]][0]:
                    simm[pair_tuple][v[1]] = v
                    found['left'].add(v[1])
                    found['right'].add(v[2])
                    compPairs[pair_tuple].append([v[1], v[2]])
        s = []
        for mol_x in simm[pair_tuple]:
            s.append(simm[pair_tuple][mol_x][0])
        if len(s) > 0:
            ss[pair_tuple] = sum(s)/len(s)
        else:
            ss[pair_tuple] = 0.0
    S1 = math.sqrt(ss[pairs[0]]**2 + ss[pairs[3]]**2)/math.sqrt(2)
    S2 = math.sqrt(ss[pairs[1]]**2 + ss[pairs[2]]**2)/math.sqrt(2)

    return(S1, S2, compPairs)

def get_morgan_fp(mol):
    mol = get_rdkit_mol(mol)
    Chem.SanitizeMol(mol)
    info1 = {}
    fpM = AllChem.GetMorganFingerprint(mol, 8, bitInfo=info1, invariants=AllChem.GetConnectivityInvariants(mol, includeRingMembership=False))
    return fpM, Chem.MolToSmiles(mol), mol.GetNumAtoms(), info1

def bulkTani(targetFp, fp, rxn_ids):
    similarity_list = DataStructs.BulkTanimotoSimilarity(targetFp, list(fp))
    dist={}
    for i in sorted(range(0, len(similarity_list))):
        dist[rxn_ids[i]] = similarity_list[i]
    return dist
