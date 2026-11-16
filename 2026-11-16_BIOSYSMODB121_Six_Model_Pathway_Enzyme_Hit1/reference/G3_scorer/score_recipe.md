# G3 score recipe (FROZEN -- teacher adjudications D1-D6 applied 2026-09-28)

Status: FROZEN_G3 (approval sha 1fa908f5ff1caad1f0cb475e820309f0b6431be4e613d51a8548088399c1a5d0).
No real model answer has been scored by this code at any point: it has only
ever seen local mocks (mocks/).

## 1. Teacher-fixed (immutable)

- Science = 0.45*Pathway + 0.10*SMILES + 0.20*Enzyme/EC/pair + 0.15*Microbial
  identity + 0.10*Traits; every layer normalized 0..100. Weights may not change.
- Evidence verifiability is an INDEPENDENT axis (verified_correct /
  unverified_correct / evidence_hallucination); it never mixes into science.
- Engineering is independent: JSON syntax, business-object form and schema
  validity are reported separately (three rates, never merged).
- null is a recall miss and never an overclaim; a wrong non-null answered with
  high confidence and without resolvable evidence is counted in overclaim.
- extra JSON fields: warnings only, original text preserved, never a hard
  failure; required fields stay strict.
- smoke/pilot data never enter formal scores; the formal phase re-runs all 121
  cases with frozen parameters (5 x 121); smoke/pilot results may not be
  reused to offset formal requests.
- case_id is the gold join key: branches of one parent pollutant never share
  gold; no root-pollutant merging.

## 2. Layer definitions (implemented in scorer.py)

- Pathway: from the alignment spec (greedy max-Jaccard one-to-one on
  substrate-union-product identity sets; direction checked per side, A->B vs
  B->A never equal). Layer = mean(step recall, main-step precision,
  matched-order concordance) * 100. Missing gold steps = recall misses;
  unmatched prediction main steps = extra-step errors; steps after the main
  endpoint placed in downstream_continuation are not penalized.
- SMILES: main compounds of matched steps; primary = canonical ISOMERIC
  equality with RDKit 2026.03.5 applied identically to gold and prediction;
  achiral-canonical reported as a separate reference number. Cases whose
  gold structure is not uniquely available are out of the SMILES denominator
  (the 5 STRUCTURALLY_INDETERMINATE cases are already excluded from formal by
  G1; auxiliary carrier gaps never affect the main-chain denominator).
- Enzyme: per gold step: accepted-name membership (G1 keeps ALL accepted
  enzymes; the model returns one preferred), EC equality against the accepted
  EC set (a gold step whose only EC is NOT_OBSERVED accepts null), and the
  enzyme-microbe pair membership in the step's accepted organism set.
- Microbial identity: per gold profile: species name, strain, exact TaxID,
  genome accession (only where gold has one), culture collection handled in
  the trait/F5 axis -- each sub-score over its available denominator, never
  padded.
- Traits: two raw rates kept separate -- observed-gold ACCURACY over G1
  scoreable cells (item mask for text/boolean traits; F2/F3/F4 exact-scalar
  sub-field mask, min==max consensus scalars only, no tolerance, optimum
  columns have an EMPTY denominator and are reported as such), and
  COMPLETENESS over all profile x 15 cells. The 1161 pending range/multi-value
  cells stay out of the accuracy denominator this phase; predicted background
  is never promoted.

## 2a. Teacher-frozen adjudications (2026-09-28, D1-D6)

- D1 (traits option B): numeric accuracy contains ONLY mask-declared numeric
  cells; F2/F3/F4 item-level cells are excluded from the numeric denominator
  (the sub-field minimum/maximum CONSENSUS SCALARS mask is authoritative);
  observed preference/category WORDS are excluded and reported as
  TEXT_COVERAGE; the 1161 pending range/multi-value cells stay out;
  completeness reported separately. all_correct reaches traits=100 by this
  REDEFINITION of the scoreable set, not by reweighting (layer weights are
  teacher-fixed and untouched).
- D2: within-layer sub-indicators equal-weighted, independent (species, strain,
  TaxID, genome; enzyme name, EC, enzyme-microbe pair). Pair credit: accepted
  species/strain NAME match. ACTIVE WRONG TaxID -> IDENTITY_CONFLICT and the
  pair is WRONG even with a correct name (fabrication is punished). TaxID=null
  -> the pair may earn name credit; the TaxID sub-indicator is a recall MISS.
  Wrong-taxid-with-right-name can never buy pair credit.
- D3: Jaccard threshold 0.5; A->B != B->A; stable-id tie-break; split/merge no
  manual forgiveness; one-to-many/many-to-one matches at most one gold step.
  Recorded limitation: 0.4/0.5/0.6 are indistinguishable on the partial mock
  (constant 77.78) -> G9 must disclose; real threshold-sensitive cases are
  record-only, never mid-run retuned.
- D4: overclaims are independent reporting + evidence-axis statistics ONLY,
  never deducted from the science score; null is a recall miss and never an
  overclaim; no rule may make an honest null score worse than a fabricated
  answer.
- D5: the formal genome accession source is traits.F14.value.genome_accession
  ONLY; a present profile-level compatibility field must agree with it or the
  cell is a CONFLICT (gen_ok=0); it never acts as a second source of truth.
  Gold item values that are profile identity tokens are not genome claims.
- D6: the main SMILES score is ALWAYS canonical isomeric; achiral-canonical is
  appendix + sensitivity reference only.

## 2b. CONTROLLED_INPUT scoring behavior (repair e20a676d, applied 2026-09-28)

The scorer LOADS G2_questions/controlled_input_scoring_mask.tsv at import
(20 rows / 14 cases) and applies it in step alignment ONLY:
- a gold side whose entities are all disclosed controlled names and whose
  prediction carries no valid structure on that side is NEUTRAL: overlap = 1.0
  by definition but excluded from the step's autonomous-evidence mean;
- both sides neutral => the pair has zero autonomous evidence => cannot MATCH
  (mere repetition of disclosed names never earns pathway recall and never
  forms a complete step);
- a MATCH still requires every NON-neutral side >= 0.5 (direction/structure/
  other entities are scored normally);
- prediction structure always keeps full authority: a WRONG or MISSING (bad)
  SMILES on a controlled entity is never exempted;
- controlled names without structure are counted and dropped from keying
  (report fields: controlled_name_repetitions, controlled_name_recall_excluded,
  disclosed_atoms_in_case);
- scope is exact case_id + exact normalized token: no global exemption, no
  substring match, the same name in another case scores normally;
- gold steps are never deleted and the recall denominator never shrinks.

Proven by controlled_input fixtures f1-f5 + empty-mask behavioral probe in
the independent validator (rule_fixtures/controlled_input_*.json).

## 3. Formerly pending items now resolved (historical record)

See G3_PREPARATION_REPORT.md OPEN DECISIONS: within-layer subindicator
weights (currently equal weights as the contract 9.5 recommended baseline),
the trait 10% composition, the overclaim penalty shape, alignment thresholds
and split/merge magnitudes, and the isomeric-vs-achiral presentation. ALL SIX
were adjudicated D1-D6 by the teacher on 2026-09-28 and are implemented per
section 2a; this section is kept as the historical record of what was once
candidate.
