#!/usr/bin/env python3
"""
Build PHN Access & Navigation Barriers Index (Project 5).

Uses PHN-level GP + BreastScreen data from MASTER_DATASET.
CALD components are placeholders until Census PHN aggregation is added —
see 03_Analysis/ROADMAP.md for data acquisition steps.
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "MASTER_DATASET.xlsx"
OUT = ROOT / "02_CleanData" / "phn_access_barriers_index.csv"

# NSW-wide context (from original analysis) — replace with PHN-level when available
NSW_CONTEXT = {
    "pct_overseas_born": 0.3461,
    "pct_recent_migrants": 0.2105,
    "pct_non_english_households": 0.0448,
    "family_complexity": 0.7505,
    "delayed_gp_access": 0.292,
}


def min_max_scale(series: pd.Series, higher_is_barrier: bool = True) -> pd.Series:
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series(50.0, index=series.index)
    scaled = (series - lo) / (hi - lo) * 100
    return scaled if higher_is_barrier else (100 - scaled)


def main() -> None:
    phn = pd.read_excel(MASTER, sheet_name="PHN", header=1)
    phn.columns = [str(c).strip().lower() for c in phn.columns]
    phn = phn.rename(
        columns={
            "primary health networks (phn)": "phn",
            "gp services per 100 people": "gp_services_per_100",
            "breastscreen participation (%)": "breastscreen_pct",
            "breastscreen participation": "breastscreen_pct",
        }
    )

    # Barrier components available now
    phn["barrier_low_screening"] = min_max_scale(
        100 - phn["breastscreen_pct"], higher_is_barrier=True
    )
    phn["barrier_high_gp_low_yield"] = min_max_scale(
        phn["gp_services_per_100"] / phn["breastscreen_pct"].clip(lower=1),
        higher_is_barrier=True,
    )

    # Placeholder: apply NSW average to all PHNs until PHN Census join
    for key, val in NSW_CONTEXT.items():
        phn[key] = val

    phn["barrier_overseas_born"] = min_max_scale(phn["pct_overseas_born"], True)
    phn["barrier_recent_migrants"] = min_max_scale(phn["pct_recent_migrants"], True)
    phn["barrier_non_english"] = min_max_scale(phn["pct_non_english_households"], True)
    phn["barrier_family_complexity"] = min_max_scale(phn["family_complexity"], True)
    phn["barrier_delayed_gp"] = min_max_scale(phn["delayed_gp_access"], True)

    component_cols = [
        "barrier_low_screening",
        "barrier_high_gp_low_yield",
        "barrier_overseas_born",
        "barrier_recent_migrants",
        "barrier_non_english",
        "barrier_family_complexity",
        "barrier_delayed_gp",
    ]

    # Weight screening + GP mismatch more heavily (data we trust at PHN level)
    weights = {
        "barrier_low_screening": 2.0,
        "barrier_high_gp_low_yield": 2.0,
        "barrier_overseas_born": 1.0,
        "barrier_recent_migrants": 1.0,
        "barrier_non_english": 1.0,
        "barrier_family_complexity": 1.0,
        "barrier_delayed_gp": 1.0,
    }
    weight_sum = sum(weights.values())
    phn["access_barriers_index"] = sum(
        phn[c] * weights[c] for c in component_cols
    ) / weight_sum

    phn["index_rank"] = phn["access_barriers_index"].rank(ascending=False, method="min").astype(int)
    phn = phn.sort_values("access_barriers_index", ascending=False)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    phn.to_csv(OUT, index=False, float_format="%.2f")

    print(f"Wrote {OUT}\n")
    print("Top 5 PHNs by access barriers index:")
    print(
        phn[["phn", "access_barriers_index", "index_rank", "breastscreen_pct", "gp_services_per_100"]]
        .head()
        .to_string(index=False)
    )
    print(
        "\nNote: CALD components currently use NSW-wide averages. "
        "Replace with PHN-level Census data for final report."
    )


if __name__ == "__main__":
    main()
