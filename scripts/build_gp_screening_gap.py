#!/usr/bin/env python3
"""
GP utilisation vs preventive screening gap analysis.

Combines Medicare GP service rates (MASTER_DATASET) with three organised
screening programs (BreastScreen, NBCSP bowel, NCSP cervical) from CAN114.

Higher gp_screening_gap = more GP visits relative to screening uptake
(a proxy for the GP–preventive care disconnect).
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "MASTER_DATASET.xlsx"
SCREENING = ROOT / "02_CleanData" / "preventive_screening_phn_nsw.csv"
OUT = ROOT / "02_CleanData" / "phn_gp_screening_gap.csv"
REPORT_DIR = ROOT / "03_Analysis" / "Project3"


def min_max_scale(series: pd.Series) -> pd.Series:
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series(50.0, index=series.index)
    return (series - lo) / (hi - lo) * 100


def gap_flag(row: pd.Series, gp_median: float, screen_median: float) -> str:
    high_gp = row["gp_services_per_100"] >= gp_median
    low_screen = row["mean_screening_pct"] <= screen_median
    if high_gp and low_screen:
        return "High GP / low screening"
    if high_gp and not low_screen:
        return "High GP / higher screening"
    if not high_gp and low_screen:
        return "Lower GP / low screening"
    return "Lower GP / higher screening"


def main() -> None:
    phn = pd.read_excel(MASTER, sheet_name="PHN", header=1)
    phn.columns = [str(c).strip().lower() for c in phn.columns]
    phn = phn.rename(
        columns={
            "primary health networks (phn)": "phn",
            "gp services per 100 people": "gp_services_per_100",
            "breastscreen participation (%)": "breastscreen_master_pct",
        }
    )

    screening = pd.read_csv(SCREENING)
    df = phn.merge(
        screening[
            [
                "phn",
                "phn_code",
                "breastscreen_pct",
                "cervical_pct",
                "bowel_pct",
            ]
        ],
        on="phn",
        how="left",
    )

    # Prefer CAN114 breast data for consistency across programs; fall back to master
    df["breastscreen_pct"] = df["breastscreen_pct"].fillna(df["breastscreen_master_pct"])
    df = df.drop(columns=["breastscreen_master_pct"])

    df["mean_screening_pct"] = df[["breastscreen_pct", "cervical_pct", "bowel_pct"]].mean(axis=1).round(2)
    df["min_screening_pct"] = df[["breastscreen_pct", "cervical_pct", "bowel_pct"]].min(axis=1).round(2)

    # Core gap metric: GP utilisation relative to average screening uptake
    df["gp_screening_gap"] = (df["gp_services_per_100"] / df["mean_screening_pct"]).round(2)
    df["gp_screening_gap_index"] = min_max_scale(df["gp_screening_gap"]).round(1)
    df["gap_rank"] = df["gp_screening_gap"].rank(ascending=False, method="min").astype(int)

    gp_med = df["gp_services_per_100"].median()
    screen_med = df["mean_screening_pct"].median()
    df["quadrant"] = df.apply(gap_flag, axis=1, gp_median=gp_med, screen_median=screen_med)

    # Program-specific gaps (GP vs each screening type)
    for prog in ("breastscreen_pct", "cervical_pct", "bowel_pct"):
        short = prog.replace("_pct", "")
        df[f"gp_vs_{short}"] = (df["gp_services_per_100"] / df[prog]).round(2)

    df = df.sort_values("gp_screening_gap", ascending=False)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False, float_format="%.2f")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    summary = df[
        [
            "phn",
            "gp_services_per_100",
            "breastscreen_pct",
            "bowel_pct",
            "cervical_pct",
            "mean_screening_pct",
            "gp_screening_gap",
            "gap_rank",
            "quadrant",
        ]
    ].copy()
    summary.to_csv(REPORT_DIR / "summary_table.csv", index=False, float_format="%.2f")

    print(f"Wrote {OUT}\n")
    print("Top 5 PHNs by GP–screening gap (high GP use, lower screening):")
    print(
        summary.head()[
            [
                "phn",
                "gp_services_per_100",
                "mean_screening_pct",
                "breastscreen_pct",
                "bowel_pct",
                "cervical_pct",
                "gp_screening_gap",
            ]
        ].to_string(index=False)
    )
    print("\nQuadrant counts:")
    print(df["quadrant"].value_counts().to_string())


if __name__ == "__main__":
    main()
