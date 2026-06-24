# References

## Primary data sources

### 1. GP service utilisation by PHN

**Australian Institute of Health and Welfare (AIHW).** *Primary health care: Medicare Benefits Schedule and other universal health-related services* — Data tables **PHC 019** (2017–18 to 2024–25).

- **File:** `01_RawData/aihw-phc-019-data-tables-1718-2425.xlsx`
- **Metric:** Medicare-billed GP consultation services per 100 population by Primary Health Network (PHN)
- **URL:** https://www.aihw.gov.au/reports/primary-health-care/primary-health-care/latest-release

### 2. BreastScreen participation by PHN

**AIHW.** *BreastScreen Australia monitoring* and supplementary data tables.

- **Files:** `AIHW-CAN-158-Access-to-BreastScreen-Australia-screening-services-2024-02-16.xlsx`; `AIHW-CAN-165-Supplementary_data_tables_breast_2025_screening.xls`
- **Metric:** Participation rate (%) among eligible women aged 50–74 by PHN
- **URL:** https://www.aihw.gov.au/reports/cancer-screening/breastscreen-australia-monitoring/latest-release

### 3. Multi-program screening by PHN

**AIHW.** Cancer screening quarterly data tables **CAN114** (July 2023 release).

- **File:** `01_RawData/AIHW-CAN114-Cancer-screening-quarterly-data-tables_14072023.xlsx`
- **Sheets used:**
  - `BreastScreen, PHN` — women aged 50–74
  - `NBCSP, PHN` — National Bowel Cancer Screening Program, people aged 50–74
  - `NCSP, PHN` — National Cervical Screening Program, ages 25–74 summary band
- **Use:** GP–screening gap analysis (`02_CleanData/phn_gp_screening_gap.csv`); SA3 BreastScreen (Project 1)

### 4. BreastScreen at SA3 (Project 1)

**AIHW.** Cancer screening quarterly data tables **CAN114**.

- **File:** `01_RawData/AIHW-CAN114-Cancer-screening-quarterly-data-tables_14072023.xlsx`
- **Sheet:** `BreastScreen, SA3 2016`
- **Use:** SA3-level BreastScreen participation for Western/SW Sydney focus areas

### 5. Cultural diversity context indicators (NSW state level)

**Australian Bureau of Statistics (ABS).** *Census of Population and Housing, 2021* — General Community Profile (GCP), New South Wales.

- **File:** `01_RawData/GCP_1.xlsx`
- **URL:** https://www.abs.gov.au/census/find-census-data/community-profiles/2021

| Indicator | Value | ABS table | Definition used in this project |
|-----------|------:|-----------|----------------------------------|
| Overseas-born population | 34.6% | **G09c** (Country of birth) | Persons born outside Australia ÷ total NSW persons |
| Recent overseas arrivals | 21.1% | **G10** (Year of arrival) | Overseas-born persons who arrived in **2016–2021** ÷ overseas-born persons *(not share of total NSW population)* |
| Limited English proficiency | 4.5% | **G13c** (Language at home × English proficiency) | Persons who use a language other than English at home and report speaking English **“not well” or “not at all”** ÷ total NSW persons |
| Family complexity (derived) | 75.1% | **G29** (Family composition), derived | Persons in families who are **not** in a “couple family with no children” ÷ all persons in families |

> **Note:** Context indicators describe NSW as a whole. They do not replace PHN-level CALD analysis. SA3/LGA Census tables are planned for follow-on work (see `03_Analysis/ROADMAP.md`).

### 6. Delayed GP access (equity context)

**Australian Bureau of Statistics (ABS).** *Patient Experiences, Australia* — 2023–24 financial year.

- **Metric:** Persons aged 15+ who **delayed or did not see a GP** when needed in the last 12 months
- **Value used:** **29.2%** (Australia, national — not NSW-specific)
- **URL:** https://www.abs.gov.au/statistics/health/health-services/patient-experiences/2023-24

> **Correction (June 2025):** An earlier draft used **34.4%**, which matched the national rate for **delayed mental health care**, not GP access. The figure has been corrected to **29.2%** from the ABS 2023–24 release.

---

## Definitions

- **GP services per 100 people:** Count of Medicare Benefits Schedule (MBS) billed GP consultation services per 100 population in a reporting year. This is a *utilisation rate*, not a count of GP doctors.
- **BreastScreen participation (%):** Proportion of eligible women (typically 50–74) who participated in BreastScreen Australia in the reporting period.
- **Bowel screening participation (%):** NBCSP participation among eligible people aged 50–74 (CAN114).
- **Cervical screening participation (%):** NCSP participation among eligible people aged 25–74 (CAN114).
- **GP–screening gap:** GP services per 100 population divided by the mean of three screening participation rates; higher values indicate more GP activity relative to organised screening uptake.
- **PHN:** Primary Health Network — regional primary care commissioning boundary.

---

## Suggested citation

> Preventive Healthcare Access Across NSW Primary Health Networks: A public health equity analysis using ABS Census 2021 and AIHW Medicare/BreastScreen data. PHN-level GP utilisation and BreastScreen participation, with NSW cultural diversity and access context indicators from ABS GCP tables and the ABS Patient Experience Survey.
