import base64
import json
import mimetypes
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CASE_DIR = PROJECT_ROOT / "cases" / "case1"
IMAGE_PATH = CASE_DIR / "raw_figure.png"
OUTPUT_PATH = CASE_DIR / "llm_output.json"


# OpenAI Structured Outputs is stricter than general JSON Schema.
# In particular, object "map" shapes are problematic here, so we ask
# the model for risk table rows as an array of objects, then convert
# them back into the dict shape used by the rest of this project.

PROPERTIES = {
    "num_groups": {
        "type": "integer",
        "description": "Number of Kaplan–Meier curves/groups visible in the figure."
    },
    "group_names": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Group names exactly as visible in the image, legend, or risk table labels."
    },
    "x_axis_label": {
        "type": ["string", "null"],
        "description": "The x-axis label if readable."
    },
    "x_axis_max": {
        "type": ["number", "null"],
        "description": "Maximum x-axis value if readable."
    },
    "y_axis_scale": {
        "type": "string",
        "description": "Use '0-100' if the y-axis is in percent, '0-1' if in proportions, or 'unknown' if uncertain."
    },
    "has_risk_table": {
        "type": "boolean",
        "description": "Whether the figure includes a visible number-at-risk table."
    },
    "risk_table_times": {
        "type": "array",
        "items": {"type": "number"},
        "description": "Time points shown above or aligned with the number-at-risk table."
    },
    "risk_table_entries": {
        "type": "array",
        "description": "Rows from the visible number-at-risk table.",
        "items": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "group_name": {
                    "type": "string"
                },
                "values": {
                    "type": "array",
                    "items": {"type": "integer"}
                }
            },
            "required": ["group_name", "values"]
        }
    },
    "legend_info": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "curve_colors_detected": {
                "type": "array",
                "items": {"type": "string"}
            },
            "group_color_mapping_confirmed": {
                "type": "boolean"
            },
            "note": {
                "type": "string"
            }
        },
        "required": [
            "curve_colors_detected",
            "group_color_mapping_confirmed",
            "note"
        ]
    },
    "curve_quality_flags": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Short notes about uncertainty, ambiguity, missing labels, or likely OCR issues."
    }
}

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": PROPERTIES,
    "required": list(PROPERTIES.keys())
}


def encode_image_as_data_url(image_path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(str(image_path))
    if mime_type is None:
        mime_type = "image/png"

    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime_type};base64,{b64}"


def normalize_output(parsed: dict) -> dict:
    entries = parsed.pop("risk_table_entries", [])
    risk_table_values = {}

    for entry in entries:
        group_name = entry.get("group_name", "").strip()
        values = entry.get("values", [])
        if group_name:
            risk_table_values[group_name] = values

    parsed["risk_table_values"] = risk_table_values
    return parsed


def main() -> None:
    load_dotenv()

    if not IMAGE_PATH.exists():
        raise FileNotFoundError(f"Image not found: {IMAGE_PATH}")

    client = OpenAI()
    image_data_url = encode_image_as_data_url(IMAGE_PATH)

    system_prompt = """
You are an expert biomedical figure extraction assistant.

Your task is to read a Kaplan–Meier survival plot image and return ONLY structured data
matching the required schema.

Rules:
1. Do not guess beyond what is visible in the image.
2. If a value is unreadable or not visible, return null, an empty list, or an empty object as appropriate.
3. Prefer exact visible text from the figure.
4. If the risk table is visible, extract the times and counts carefully.
5. If treatment-to-color mapping is uncertain, set group_color_mapping_confirmed to false and explain in legend_info.note.
6. Include uncertainty notes in curve_quality_flags.
7. This image may be a cropped panel from a larger figure. Do not invent missing legend details.
8. For the risk table, return rows in risk_table_entries as:
   [{"group_name": "...", "values": [..]}]
""".strip()

    user_prompt = """
Extract structured metadata from this Kaplan–Meier curve image.

Focus on:
- number of groups
- group names
- x-axis label
- x-axis maximum
- y-axis scale
- whether a number-at-risk table is present
- risk table time points
- risk table rows as risk_table_entries
- visible curve colors
- uncertainty notes

Return valid JSON only.
""".strip()

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": [{"type": "input_text", "text": system_prompt}],
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": user_prompt},
                    {"type": "input_image", "image_url": image_data_url},
                ],
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "km_curve_extraction",
                "strict": True,
                "schema": SCHEMA,
            }
        },
    )

    parsed = json.loads(response.output_text)
    normalized = normalize_output(parsed)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(normalized, f, indent=2, ensure_ascii=False)

    print(f"Saved structured output to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
