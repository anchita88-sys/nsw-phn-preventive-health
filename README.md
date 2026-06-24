# Preventive Healthcare Access Across NSW PHNs

Public health equity analysis comparing GP service utilisation and BreastScreen participation across NSW Primary Health Networks.

**Live report:** https://anchita88-sys.github.io/nsw-phn-preventive-health/

## Recommended format for audiences

**Use the narrative report — not Tableau.**

| Format | File | Best for |
|--------|------|----------|
| **Web report (recommended)** | `05_PolicyBrief/narrative-report.html` | Reading in browser; charts inline; print to PDF |
| **Google Docs source** | `05_PolicyBrief/narrative-report.md` | Copy-paste into Google Docs; add chart screenshots |
| Interactive dashboard (legacy) | `04_Dashboard/index.html` | Optional; superseded by narrative report |
| Tableau workbook | `Preventive Healthcare Access Across NSW PHNs (Revised).twbx` | Analyst exploration only |

### Why not Tableau for this audience?

Feedback showed dashboards confuse readers about:

- What to read first  
- What metrics mean (especially “GP services per 100 people”)  
- Where each chart’s data comes from  
- Why context indicators appear without explanation  

A **linear report** (Google Doc / PDF / HTML) answers those questions in order.

### Quick start

1. Open `05_PolicyBrief/narrative-report.html` in Chrome or Safari  
2. Or copy `narrative-report.md` into Google Docs and export as PDF  
3. For presentations: use Section 1 (summary) + Section 5 (findings) + one chart

## Project structure

| Folder | Contents |
|--------|----------|
| `01_RawData/` | AIHW and ABS source files |
| `04_Dashboard/` | Legacy interactive dashboard |
| `05_PolicyBrief/` | **Narrative report (primary deliverable)** |
| `06_References/` | Data citations and definitions |
| `MASTER_DATASET.xlsx` | Combined PHN + NSW context data |

## Research question

How does preventive healthcare access and engagement vary across NSW PHNs within the context of cultural diversity and migration patterns?

## Key metric clarification

**“GP services per 100 people”** = Medicare-billed GP **consultations** per 100 residents per year (~7–8 visits per person on average at 750/100). It is **not** the number of GPs per person.
