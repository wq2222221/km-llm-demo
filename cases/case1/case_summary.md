# ICON7 Case Summary

This cached case is based on **ICON7 Figure 2C**, which shows **overall survival in the predefined high-risk subgroup** of women with newly diagnosed ovarian cancer.

## Comparison
- Standard chemotherapy
- Chemotherapy + bevacizumab

## What is shown on the website
- Raw Kaplan–Meier figure
- LLM-extracted structured metadata
- Approximate manually seeded curve points
- Cached log-rank result for the published comparison

## Important notes
- The current `corrected_points.csv` is an initial manually seeded approximation from the cropped screenshot, not an exact digitization.
- The paper reports a **log-rank p-value of 0.03** for the high-risk subgroup overall survival comparison.
- The displayed `test_statistic` in `logrank_result.json` is an approximate back-calculation from the reported p-value, included only so the demo site can render a numeric statistic.
- Curve-to-treatment color mapping was not fully confirmed from the cropped figure alone and should be treated cautiously until checked against the full article figure/legend.
