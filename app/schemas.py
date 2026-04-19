from pydantic import BaseModel, Field
from typing import Any


class CaseMeta(BaseModel):
    case_id: str
    title: str
    summary: str
    disease: str | None = None
    treatments: list[str] = Field(default_factory=list)
    source_note: str | None = None
    has_extra_credit: bool = False


class LogRankResult(BaseModel):
    test_statistic: float
    p_value: float
    note: str | None = None


class CurvePoint(BaseModel):
    time: float
    survival: float
    group: str


class LLMExtractionOutput(BaseModel):
    num_groups: int
    group_names: list[str]
    x_axis_label: str | None = None
    x_axis_max: float | None = None
    y_axis_scale: str | None = None
    has_risk_table: bool = False
    risk_table_times: list[float] = Field(default_factory=list)
    risk_table_values: dict[str, list[int]] = Field(default_factory=dict)
    legend_info: dict[str, Any] = Field(default_factory=dict)
    curve_quality_flags: list[str] = Field(default_factory=list)
