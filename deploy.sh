#!/bin/bash
# Deploy this project to GitHub and enable GitHub Pages.
# Run: bash deploy.sh

set -e
cd "$(dirname "$0")"

REPO="https://github.com/anchita88-sys/nsw-phn-preventive-health.git"
GH="${GH_BIN:-/tmp/gh_2.67.0_macOS_arm64/bin/gh}"

echo "=== Step 1: GitHub login (one-time) ==="
if ! $GH auth status >/dev/null 2>&1; then
  echo "A browser window will open — sign in to GitHub as anchita88-sys."
  $GH auth login -h github.com -p https -w
fi

echo ""
echo "=== Step 2: Push project ==="
if [ ! -d .git ]; then
  git init
  git branch -M main
fi
git add README.md PUBLISHING.md .gitignore docs/ 05_PolicyBrief/ 06_References/ MASTER_DATASET.xlsx 04_Dashboard/index.html
if git diff --cached --quiet; then
  echo "No new changes to commit."
else
  git commit -m "Publish NSW PHN preventive healthcare equity report"
fi
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO"
git push -u origin main

echo ""
echo "=== Step 3: Enable GitHub Pages (/docs folder) ==="
$GH api repos/anchita88-sys/nsw-phn-preventive-health/pages \
  -X POST \
  -f build_type=legacy \
  -f source[branch]=main \
  -f source[path]=/docs 2>/dev/null \
  || $GH api repos/anchita88-sys/nsw-phn-preventive-health/pages \
  -X PUT \
  -f build_type=legacy \
  -f source[branch]=main \
  -f source[path]=/docs

echo ""
echo "=== Done ==="
echo "Repo:  https://github.com/anchita88-sys/nsw-phn-preventive-health"
echo "Site:  https://anchita88-sys.github.io/nsw-phn-preventive-health/"
echo "(Pages may take 1–3 minutes to go live)"
