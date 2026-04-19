from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CASE_DIR = PROJECT_ROOT / "cases" / "case1"
CSV_PATH = CASE_DIR / "reconstructed_ipd.csv"
OUT_PATH = CASE_DIR / "km_plot.png"

def main():
    df = pd.read_csv(CSV_PATH)
    required = {"time", "status", "arm"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    plt.figure(figsize=(8, 5.5))
    for arm, gdf in df.groupby("arm", sort=False):
        kmf = KaplanMeierFitter(label=arm)
        kmf.fit(gdf["time"], event_observed=gdf["status"])
        kmf.plot(ci_show=False)

    plt.xlabel("Months since randomisation")
    plt.ylabel("Overall survival probability")
    plt.title("Approximate KM plot from reconstructed pseudo-IPD")
    plt.xlim(left=0)
    plt.ylim(0, 1.0)
    plt.tight_layout()
    plt.savefig(OUT_PATH, dpi=200)
    print(f"Saved KM plot to: {OUT_PATH}")

if __name__ == "__main__":
    main()
