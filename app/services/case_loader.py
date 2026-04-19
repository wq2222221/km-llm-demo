import json
from pathlib import Path
from app.config import CASES_DIR
from app.schemas import CaseMeta, LogRankResult


def list_case_dirs() -> list[Path]:
    if not CASES_DIR.exists():
        return []
    return sorted([p for p in CASES_DIR.iterdir() if p.is_dir()])


def load_case_meta(case_id: str) -> CaseMeta:
    case_dir = CASES_DIR / case_id
    meta_path = case_dir / "meta.json"
    with open(meta_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return CaseMeta(**data)


def load_logrank_result(case_id: str) -> LogRankResult | None:
    path = CASES_DIR / case_id / "logrank_result.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return LogRankResult(**data)


def load_case_summary(case_id: str) -> str | None:
    path = CASES_DIR / case_id / "case_summary.md"
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def list_cases() -> list[CaseMeta]:
    cases: list[CaseMeta] = []
    for case_dir in list_case_dirs():
        meta_path = case_dir / "meta.json"
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                cases.append(CaseMeta(**json.load(f)))
    return cases
