from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CASE_DIR = PROJECT_ROOT / "cases" / "case1"
CSV_PATH = CASE_DIR / "corrected_points.csv"
OUT_PATH = CASE_DIR / "km_plot.png"

def main():
    df = pd.read_csv(CSV_PATH)
    required = {"time", "survival", "group"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    plt.figure(figsize=(8, 5.5))

    for group_name, gdf in df.groupby("group", sort=False):
        gdf = gdf.sort_values("time")
        plt.step(
            gdf["time"],
            gdf["survival"],
            where="post",
            label=group_name,
        )

    plt.xlabel("Months since randomisation")
    plt.ylabel("Overall survival (%)")
    plt.title("Approximate Kaplan–Meier plot from corrected_points.csv")
    plt.xlim(left=0)
    plt.ylim(0, 100)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_PATH, dpi=200)
    print(f"Saved KM plot to: {OUT_PATH}")

if __name__ == "__main__":
    main()
