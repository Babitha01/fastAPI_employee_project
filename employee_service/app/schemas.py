from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Literal

class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    department: str = Field(min_length=1, max_length=100)
    primary_skill: str = Field(min_length=1, max_length=100)
    location: str = Field(min_length=1, max_length=100)
    work_mode: Literal["WFH", "WFO"]
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: Literal["WFH", "WFO"]
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
