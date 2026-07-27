# M3-P1-2.1 Reaction-Predictor Biological Route Selection

Date: 2026-07-27  
Status: `PILOT COMPLETE / LIU-TEACHER A-B-C SELECTION PENDING / NO IMPLEMENTATION AUTHORIZED`

This folder contains the detailed biological route-selection material prepared
for Liu-laoshi after the unified A/B/C pilot.

Teacher-facing files:

- [`M3_P1_2_1_REACTION_PREDICTOR_BIOLOGICAL_ROUTE_SELECTION_CARD_2026-07-26.md`](M3_P1_2_1_REACTION_PREDICTOR_BIOLOGICAL_ROUTE_SELECTION_CARD_2026-07-26.md):
  full auditable comparison, measured results, limitations and selection area;
- [`M3_P1_2_1_REACTION_PREDICTOR_ABC_ROUTE_TEACHER_PRESENTATION_2026-07-26.html`](M3_P1_2_1_REACTION_PREDICTOR_ABC_ROUTE_TEACHER_PRESENTATION_2026-07-26.html):
  visual meeting version.

Independent local audits are under [`audits/`](audits/). File identities are
listed in [`DELIVERABLE_SHA256SUMS.txt`](DELIVERABLE_SHA256SUMS.txt).

The pending biological choice is:

```text
A:
  professional reaction-prediction tool route

B:
  LLM candidate-reaction generation with strict validation

C:
  degradation-rule / known-pathway template route
```

The existing pilot does not authorize production code. Route A's tested
BioTransformer configuration is contract-incompatible; Route B currently
returns product-only candidates; C-exact is a known-Rhea lookup baseline and
C-generic is not yet built. Any selected next pilot still requires Huang-laoshi
authorization.
