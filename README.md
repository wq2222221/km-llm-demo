# KM-LLM Demo

A course final project website for **Option 2**:
using an LLM-assisted workflow to extract structured information from Kaplan–Meier curves, build cached demo outputs, and present an indirect comparison example.

## Project overview

This project contains two main parts:

1. **Main case demo**
   - Real Kaplan–Meier figure
   - LLM-extracted structured metadata
   - Approximate corrected curve points
   - Approximate reconstructed pseudo-IPD
   - Replotted Kaplan–Meier curve
   - Cached log-rank result

2. **Extra credit page**
   - Anchored indirect comparison setup
   - Two published studies with a common comparator
   - Approximate Bucher-style indirect comparison result

## Current project structure

```text
km-llm-project-starter/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── services/
│   │   ├── case_loader.py
│   │   └── extra_credit_loader.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── case.html
│   │   └── extra_credit.html
│   └── static/
│       └── style.css
├── cases/
│   ├── case1/
│   │   ├── raw_figure.png
│   │   ├── meta.json
│   │   ├── llm_output.json
│   │   ├── corrected_points.csv
│   │   ├── reconstructed_ipd.csv
│   │   ├── km_plot.png
│   │   ├── logrank_result.json
│   │   └── case_summary.md
│   └── extra_credit.json
├── scripts/
│   ├── extract_with_llm.py
│   ├── plot_km_from_corrected_points.py
│   └── plot_km_from_reconstructed_ipd.py
├── requirements.txt
├── Procfile
├── railway.json
├── .env.example
└── README.md
```

## Local run

Create and activate a virtual environment, then install requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Start the website locally:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## Environment variables

Create a local `.env` file based on `.env.example`.

Example:

```env
OPENAI_API_KEY=your_real_key_here
NCBI_EMAIL=your_email_here
NCBI_API_KEY=
APP_ENV=development
```

## Important safety note

Do **not** commit your real `.env` file or your real API key to GitHub.

Keep only `.env.example` in the repository.

## Cached demo design

This project is intentionally designed so that the public website can be graded using **cached outputs**.
The website does not need to expose or use a live API key at grading time.

## Railway deployment

Recommended workflow:

1. Push the project to GitHub
2. Connect the GitHub repository to Railway
3. Deploy the FastAPI service
4. Add environment variables in Railway only if needed
5. Verify that the deployed website opens normally

## Suggested submission contents

- Public website URL
- GitHub repository URL
- Source code
- Cached output files
- Screenshots of the main case and extra credit page
- Short report or PDF summary

## Project limitations

- The current `corrected_points.csv` is an approximate manually seeded curve file.
- The current `reconstructed_ipd.csv` is an approximate pseudo-IPD demo, not a formal IPDfromKM reconstruction.
- The extra credit result is a simple anchored indirect comparison based on published hazard ratios, not a full adjusted indirect treatment comparison workflow.

## Recommended final polish before submission

- Render Markdown in `case_summary.md` as HTML
- Add article links / PMID / DOI to the extra credit page
- Add a short footer with repository and deployment links
- Confirm that every file path works on the deployed website
