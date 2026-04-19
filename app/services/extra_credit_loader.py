import json
from app.config import CASES_DIR


def load_extra_credit_data() -> dict | None:
    path = CASES_DIR / "extra_credit.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
