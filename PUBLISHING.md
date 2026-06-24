# Publishing this project for your CV

## Recommended approach: GitHub + GitHub Pages

**Why this is best for a CV link**

- Free, permanent URL you control
- Looks professional to employers and grad schools
- Shows you can communicate research publicly, not just analyse data
- One link on your CV opens the full interactive report in any browser
- Optional: attach a PDF and dataset in the same repo

**Target URL:**

```
https://anchita88-sys.github.io/nsw-phn-preventive-health/
```

**Your repository:**

```
https://github.com/anchita88-sys/nsw-phn-preventive-health
```

---

## Step-by-step (about 15 minutes)

### 1. Create a GitHub account (if needed)

https://github.com/join

### 2. Create a new public repository

- Name: `nsw-phn-preventive-health` (short, readable in a CV)
- Visibility: **Public**
- Do **not** add a README on GitHub (you already have one locally)

### 3. Push this project from your Mac

Run in Terminal:

```bash
cd "/Users/anchitasood/Desktop/Projects/CALD_PreventativeCareProject"

git init
git add README.md PUBLISHING.md .gitignore docs/ 05_PolicyBrief/ 06_References/ MASTER_DATASET.xlsx 04_Dashboard/index.html
git commit -m "Publish NSW PHN preventive healthcare equity report"

git branch -M main
git remote add origin https://github.com/anchita88-sys/nsw-phn-preventive-health.git
git push -u origin main
```

To include raw data (optional, ~87 MB):

```bash
git add 01_RawData/
git commit -m "Add source data files"
git push
```

### 4. Turn on GitHub Pages

1. GitHub repo → **Settings** → **Pages**
2. **Build and deployment** → Source: **Deploy from a branch**
3. Branch: **main** → Folder: **/docs**
4. Save

After 1–3 minutes, your site is live at:

```
https://YOUR-GITHUB-USERNAME.github.io/nsw-phn-preventive-health/
```

### 5. Add a PDF (optional but good for CV)

1. Open `docs/index.html` in Chrome
2. **File → Print → Save as PDF**
3. Save as `docs/report.pdf` and push:

```bash
git add docs/report.pdf
git commit -m "Add PDF version of report"
git push
```

PDF link: `https://YOUR-GITHUB-USERNAME.github.io/nsw-phn-preventive-health/report.pdf`

---

## What to put on your CV

**Projects section (one line):**

> **Preventive Healthcare Access Across NSW PHNs** — Public health equity analysis of GP utilisation and BreastScreen participation across NSW Primary Health Networks (AIHW, ABS). [Report](https://YOUR-GITHUB-USERNAME.github.io/nsw-phn-preventive-health/) · [PDF](https://YOUR-GITHUB-USERNAME.github.io/nsw-phn-preventive-health/report.pdf) · [GitHub](https://github.com/YOUR-GITHUB-USERNAME/nsw-phn-preventive-health)

**LinkedIn / portfolio:** Use the Report link as the primary button.

---

## Other options (when to use each)

| Option | Best for | CV link example |
|--------|----------|-----------------|
| **GitHub Pages** (recommended) | Interactive report + code + data | `username.github.io/nsw-phn-preventive-health/` |
| **Google Docs (anyone with link)** | Fastest, no setup | `docs.google.com/document/d/...` |
| **Notion public page** | Pretty portfolio pages | `yourname.notion.site/...` |
| **Personal website** | If you already have one | `yourname.com/projects/nsw-phn` |
| **Zenodo** | Academic roles needing a DOI | `doi.org/10.5281/zenodo...` |
| **OSF** | Research / thesis portfolios | `osf.io/xxxxx` |

**Avoid for CV primary link:** Tableau Public (requires account to view some workbooks), private Google Drive links, local file paths.

---

## Before you go public — quick checklist

- [ ] Report reads well on mobile (open the GitHub Pages URL on your phone)
- [ ] No personal phone/email in the document unless you want them public
- [ ] References cite AIHW and ABS correctly
- [ ] Repository description on GitHub: *"Public health equity analysis — GP access & BreastScreen participation across NSW PHNs"*
- [ ] Add topics on GitHub: `public-health`, `health-equity`, `nsw`, `data-analysis`

---

## Updating later

Edit `05_PolicyBrief/narrative-report.html`, then copy to `docs/index.html`:

```bash
cp 05_PolicyBrief/narrative-report.html docs/index.html
git add docs/index.html 05_PolicyBrief/narrative-report.html
git commit -m "Update report"
git push
```

GitHub Pages rebuilds automatically within a few minutes.
