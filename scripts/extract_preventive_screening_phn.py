#!/usr/bin/env python3
"""Extract BreastScreen, NBCSP (bowel), and NCSP (cervical) participation by PHN from AIHW CAN114."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "01_RawData" / "AIHW-CAN114-Cancer-screening-quarterly-data-tables_14072023.xlsx"
OUT = ROOT / "02_CleanData" / "preventive_screening_phn_nsw.csv"


def _latest_participation_col(df: pd.DataFrame) -> str:
    pct_cols = [c for c in df.columns if "participation" in str(c).lower() and "%" in str(c)]
    if not pct_cols:
        raise ValueError("No participation (%) columns found")
    return pct_cols[-1]


def extract_bowel_phn() -> pd.DataFrame:
    df = pd.read_excel(RAW, sheet_name="NBCSP, PHN ", header=3)
    df = df.rename(
        columns={
            df.columns[0]: "state",
            df.columns[1]: "phn_code",
            df.columns[2]: "phn_name",
        }
    )
    df = df[df["state"].eq("NSW")].copy()
    col = _latest_participation_col(df)
    df["bowel_pct"] = pd.to_numeric(df[col], errors="coerce")
    df["bowel_period"] = str(col).replace("Participation (%)", "").strip() or "latest"
    return df[["phn_code", "phn_name", "bowel_pct"]].drop_duplicates()


def extract_cervical_phn() -> pd.DataFrame:
    df = pd.read_excel(RAW, sheet_name="NCSP, PHN", header=3)
    df = df.rename(
        columns={
            df.columns[0]: "state",
            df.columns[1]: "phn_code",
            df.columns[2]: "phn_name",
            df.columns[3]: "age_group",
        }
    )
    df = df[df["state"].eq("NSW")].copy()
    col = _latest_participation_col(df)
    # Use program summary age band (25–74) when available
    summary = df[df["age_group"].astype(str).str.replace("-", "–").eq("25–74")]
    if summary.empty:
        summary = df.groupby(["phn_code", "phn_name"], as_index=False)[col].mean()
        summary = summary.rename(columns={col: "cervical_pct"})
    else:
        summary = summary[["phn_code", "phn_name", col]].rename(columns={col: "cervical_pct"})
    summary["cervical_pct"] = pd.to_numeric(summary["cervical_pct"], errors="coerce").round(2)
    return summary.drop_duplicates()


def extract_breast_phn() -> pd.DataFrame:
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
    col = _latest_participation_col(df)
    summary = df[df["age_group"].astype(str).str.replace("-", "–").eq("50–74")]
    if summary.empty:
        summary = df.groupby(["phn_code", "phn_name"], as_index=False)[col].mean()
        summary = summary.rename(columns={col: "breastscreen_pct"})
    else:
        summary = summary[["phn_code", "phn_name", col]].rename(columns={col: "breastscreen_pct"})
    summary["breastscreen_pct"] = pd.to_numeric(summary["breastscreen_pct"], errors="coerce").round(2)
    return summary.drop_duplicates()


def normalise_phn_name(name: str) -> str:
    """Align CAN114 PHN names with MASTER_DATASET spelling."""
    mapping = {
        "Central and Eastern Sydney": "Central & Eastern Sydney",
        "Hunter New England and Central Coast": "Hunter New England and Central Coast",
        "South Eastern NSW": "South Eastern Sydney",
    }
    return mapping.get(str(name).strip(), str(name).strip())


def main() -> None:
    bowel = extract_bowel_phn()
    cervical = extract_cervical_phn()
    breast = extract_breast_phn()

    out = breast.merge(cervical, on=["phn_code", "phn_name"], how="outer")
    out = out.merge(bowel, on=["phn_code", "phn_name"], how="outer")
    out["phn"] = out["phn_name"].map(normalise_phn_name)
    out = out.sort_values("phn")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False, float_format="%.2f")
    print(f"Wrote {OUT} ({len(out)} PHNs)")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
