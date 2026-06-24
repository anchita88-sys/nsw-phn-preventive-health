# Analysis Roadmap: Projects 1, 3 & 5

Follow-on projects building on **Preventive Healthcare Access Across NSW PHNs**.

| # | Project | Research question | Status |
|---|---------|-------------------|--------|
| **1** | CALD disaggregation (Western & SW Sydney) | Do areas with higher cultural diversity within Western/SW Sydney PHNs have lower BreastScreen participation? | Data extracted (SA3); Census join pending |
| **3** | GP vs preventive screening gap | Where GP use is high, is breast, bowel, and cervical screening also low? | **Analysis complete** — see report below |
| **5** | PHN Access & Navigation Barriers Index | Can a composite barrier score explain variation in preventive screening across NSW PHNs? | Index built; CALD placeholders pending |

---

## GP utilisation vs preventive screening gap ✅

### Goal
Test whether the **GP–BreastScreen disconnect** from the main report extends to **bowel (NBCSP)** and **cervical (NCSP)** screening — a broader picture of preventive care conversion.

### Data used
| Source | File | Metrics |
|--------|------|---------|
| AIHW PHC 019 | `aihw-phc-019-data-tables-1718-2425.xlsx` | GP services per 100 by PHN |
| AIHW CAN114 | `AIHW-CAN114-...xlsx` | BreastScreen, NBCSP, NCSP participation by PHN |
| Master dataset | `MASTER_DATASET.xlsx` | PHN merge key |

### Key outputs
| File | Description |
|------|-------------|
| `02_CleanData/preventive_screening_phn_nsw.csv` | Three-program screening rates by PHN |
| `02_CleanData/phn_gp_screening_gap.csv` | GP–screening gap scores and quadrants |
| `02_CleanData/Project3_GP_Screening_Gap.xlsx` | Excel deliverable |
| `05_PolicyBrief/project3-gp-screening-gap.md` | Narrative report |
| `docs/project3.html` | Web report (GitHub Pages) |

### Headline finding
**South Western Sydney**, **Nepean Blue Mountains**, and **Western Sydney** rank highest on GP–screening gap. Bowel participation is especially low (36–39%) despite GP rates above 696/100.

### Scripts
```bash
python scripts/extract_preventive_screening_phn.py
python scripts/build_gp_screening_gap.py
```

---

## Project 1 — CALD disaggregation within Western & SW Sydney

### Goal
Move from **PHN-level** analysis to **SA3/LGA-level** within the two lowest-screening PHNs:
- Western Sydney (PHN103)
- South Western Sydney (PHN105)

### Data you already have
| Source | File | Geography | Use |
|--------|------|-----------|-----|
| AIHW CAN114 | `AIHW-CAN114-...xlsx` | **SA3**, PHN | BreastScreen participation by SA3 |
| AIHW CAN114 | same | PHN | PHN-level validation |
| ABS Census GCP | `GCP_1.xlsx` (NSW) | **State only** | Not granular enough — need SA3/LGA download |

### Data to acquire (one-time ABS download)
From [ABS Census 2021 General Community Profile](https://www.abs.gov.au/census/find-census-data/community-profiles):
- **GCP SA3 (NSW)** or **GCP LGA (NSW)** for Greater Sydney
- Tables needed: **G09** (country of birth), **G13** (language), **G25/G36** (family/household)

### Analysis steps
1. Extract SA3 BreastScreen participation from CAN114 → `02_CleanData/breastscreen_sa3_nsw.csv` ✓
2. Map SA3 → Western Sydney / SW Sydney PHN (ABS correspondence or AIHW PHN-SA3 mapping)
3. Join Census CALD indicators (% overseas-born, % non-English at home) by SA3
4. Scatter/bar charts: CALD % vs participation within focus PHNs
5. Narrative report (same format as main report)

### Deliverable
- Report: *CALD diversity and BreastScreen participation in Western Sydney*
- New portfolio project entry + GitHub repo (optional separate repo)

---

## Project 5 — PHN Access & Navigation Barriers Index

### Goal
Build a **composite index (0–100)** for each NSW PHN where **higher score = greater access/navigation barriers**, then test whether it correlates with low BreastScreen participation.

### Index components (proposed)

| Component | Direction | Source | PHN-level? |
|-----------|-----------|--------|------------|
| % overseas-born | Higher = barrier | ABS Census | Needs SA3→PHN aggregation |
| % recent migrants (10 yr) | Higher = barrier | ABS Census | Needs extraction |
| % non-English households | Higher = barrier | ABS Census | Needs extraction |
| Family complexity indicator | Higher = barrier | ABS / derived | Needs extraction |
| Delayed GP access when needed | Higher = barrier | ABS Patient Experiences 2023–24 | **29.2% national** (not PHN-level); used as NSW-wide placeholder in index |
| Low BreastScreen participation | Higher = barrier | AIHW CAN114 / master dataset | **Yes — ready** |

**Standardisation:** Min–max scale each indicator across 10 NSW PHNs (0 = lowest barrier, 100 = highest), then average (or weighted average).

### Hypothesis
PHNs with **higher barrier index** will have **lower BreastScreen participation**, including Western/SW Sydney ranking highest on barriers.

### Analysis steps
1. Compile PHN-level screening + GP data (from `MASTER_DATASET.xlsx`) ✓
2. Extract / import PHN-level CALD indicators from Census
3. Calculate composite index → `02_CleanData/phn_access_barriers_index.csv` ✓
4. Correlate index with BreastScreen participation
5. Rank PHNs; interpret Western Sydney vs Murrumbidgee contrast
6. Narrative report with methodology appendix

### Deliverable
- Report: *PHN access barriers index and preventive screening in NSW*
- Methodology table showing exact formula and data sources

---

## Suggested order of work

```
Done       GP vs multi-program screening gap
Week 1–2   Project 5 foundation (PHN index + GP/screening correlation) ✓ partial
Week 2–3   Download ABS SA3/LGA Census for Sydney → feed Project 1 & 5
Week 3–4   Project 1 SA3 analysis (Western/SW Sydney focus)
Week 4–5   Finalise remaining reports; update portfolio
```

---

## Scripts in this repo

```bash
pip install -r requirements.txt
python scripts/extract_breastscreen_sa3.py      # Project 1
python scripts/extract_preventive_screening_phn.py
python scripts/build_gp_screening_gap.py
python scripts/build_access_index.py            # Project 5
```

Outputs go to `02_CleanData/`.
