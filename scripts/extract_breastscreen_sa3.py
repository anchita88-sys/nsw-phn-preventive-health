#!/usr/bin/env python3
"""Extract BreastScreen participation by SA3 and PHN from AIHW CAN114."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "01_RawData" / "AIHW-CAN114-Cancer-screening-quarterly-data-tables_14072023.xlsx"
OUT_DIR = ROOT / "02_CleanData"
OUT_DIR.mkdir(parents=True, exist_ok=True)

WESTERN_SYDNEY_PHNS = {"Western Sydney", "South Western Sydney"}

# SA3 names commonly associated with Western / SW Sydney PHN areas (expand as needed)
FOCUS_KEYWORDS = [
    "Blacktown",
    "Parramatta",
    "Fairfield",
    "Bankstown",
    "Liverpool",
    "Campbelltown",
    "Penrith",
    "Auburn",
    "Canterbury",
    "Holroyd",
    "Merrylands",
    "Cabramatta",
    "Mount Druitt",
    "St Marys",
]


def latest_participation(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate age groups; use last available participation column."""
    pct_cols = [c for c in df.columns if "participation" in str(c).lower() and "%" in str(c)]
    pop_cols = [c for c in df.columns if str(c).lower().startswith("population")]
    part_cols = [c for c in df.columns if str(c).lower().startswith("participants")]

    if pct_cols:
        df = df.copy()
        df["participation_pct"] = pd.to_numeric(df[pct_cols[-1]], errors="coerce")
    elif part_cols and pop_cols:
        p = pd.to_numeric(df[part_cols[-1]], errors="coerce")
        n = pd.to_numeric(df[pop_cols[-1]], errors="coerce")
        df = df.copy()
        df["participation_pct"] = (p / n * 100).round(2)
    return df


def extract_phn() -> pd.DataFrame:
    df = pd.read_excel(RAW, sheet_name="BreastScreen, PHN", header=3)
    df = df.rename(
        columns={
            df.columns[0]: "state",
            df.columns[1]: "phn_code",
            df.columns[2]: "phn_name",
            df.columns[3]: "age_group",
        }
    )
    df = df[df["state"].eq("NSW")].copy()
    df = latest_participation(df)
    out = (
        df.groupby(["phn_code", "phn_name"], as_index=False)["participation_pct"]
        .mean()
        .round(2)
        .sort_values("participation_pct")
    )
    return out


def extract_sa3() -> pd.DataFrame:
    df = pd.read_excel(RAW, sheet_name="BreastScreen, SA3 2016", header=3)
    df = df.rename(
        columns={
            df.columns[0]: "state",
            df.columns[1]: "sa3_code",
            df.columns[2]: "sa3_name",
            df.columns[3]: "age_group",
        }
    )
    df = df[df["state"].eq("NSW")].copy()
    df = latest_participation(df)
    out = (
        df.groupby(["sa3_code", "sa3_name"], as_index=False)["participation_pct"]
        .mean()
        .round(2)
        .sort_values("participation_pct")
    )
    out["focus_area"] = out["sa3_name"].apply(
        lambda name: any(k.lower() in str(name).lower() for k in FOCUS_KEYWORDS)
    )
    return out


def main() -> None:
    phn = extract_phn()
    sa3 = extract_sa3()
    focus = sa3[sa3["focus_area"]].copy()

    phn_path = OUT_DIR / "breastscreen_phn_nsw.csv"
    sa3_path = OUT_DIR / "breastscreen_sa3_nsw.csv"
    focus_path = OUT_DIR / "breastscreen_sa3_western_sydney_focus.csv"

    phn.to_csv(phn_path, index=False)
    sa3.to_csv(sa3_path, index=False)
    focus.to_csv(focus_path, index=False)

    print(f"Wrote {phn_path} ({len(phn)} PHNs)")
    print(f"Wrote {sa3_path} ({len(sa3)} SA3s)")
    print(f"Wrote {focus_path} ({len(focus)} focus SA3s)")
    print("\nWestern/SW Sydney PHN screening:")
    print(phn[phn["phn_name"].isin(WESTERN_SYDNEY_PHNS)].to_string(index=False))


if __name__ == "__main__":
    main()
