from pydantic import BaseModel, Field
from enum import Enum


class Confidence(str, Enum):
    confident = "confident"
    inferred = "inferred"
    unknown = "unknown"


class AxisMapping(BaseModel):
    section: str
    axis: str
    value: int = Field(ge=1, le=10)
    confidence: Confidence
    reason: str


class CrossMapping(BaseModel):
    journey_axis: str
    mechanism_axis: str
    level: int = Field(ge=0, le=3)
    confidence: Confidence
    reason: str


class MessageRequest(BaseModel):
    message: str


class MessageResponse(BaseModel):
    response: str
    mappings_updated: list[AxisMapping]
    cross_updated: list[CrossMapping]
    completion: dict[str, float]
    is_complete: bool
