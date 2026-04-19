from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import STATIC_DIR, TEMPLATES_DIR, CASES_DIR
from app.services.case_loader import (
    list_cases,
    load_case_meta,
    load_case_summary,
    load_logrank_result,
)
from app.services.extra_credit_loader import load_extra_credit_data

app = FastAPI(title="KM-LLM Demo", version="0.1.0")

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/case-files", StaticFiles(directory=str(CASES_DIR)), name="case_files")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/")
def home(request: Request):
    cases = list_cases()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"cases": cases},
    )


@app.get("/cases/{case_id}")
def case_detail(request: Request, case_id: str):
    try:
        meta = load_case_meta(case_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Case not found")

    logrank = load_logrank_result(case_id)
    case_summary = load_case_summary(case_id)

    return templates.TemplateResponse(
        request=request,
        name="case.html",
        context={
            "case": meta,
            "logrank": logrank,
            "case_summary": case_summary,
            "case_id": case_id,
        },
    )


@app.get("/extra-credit")
def extra_credit(request: Request):
    data = load_extra_credit_data()
    return templates.TemplateResponse(
        request=request,
        name="extra_credit.html",
        context={"extra_credit": data},
    )
