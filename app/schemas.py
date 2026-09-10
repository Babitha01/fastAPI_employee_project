from pydantic import BaseModel, EmailStr
from typing import Literal

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: Literal["WFH", "WFO"]
class EmployeeUpdate(BaseModel):
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: Literal["WFH", "WFO"]
class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: Literal["WFH", "WFO"]
    is_active: bool
    created_at: str