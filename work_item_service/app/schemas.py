from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator

class WorkItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: str | None = None
    employee_id: int = Field(gt=0)
    status: Literal["TODO"] = "TODO"
    priority: Literal["LOW", "MEDIUM", "HIGH"] = "MEDIUM"
    due_date: datetime | None = None
    model_config = ConfigDict(str_strip_whitespace=True)
    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty")
        return value.strip()

class WorkItemResponse(BaseModel):
    id: int
    title: str
    description: str | None
    employee_id: int
    status: str
    priority: str
    due_date: datetime | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)