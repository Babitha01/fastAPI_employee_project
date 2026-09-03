from pydantic import BaseModel,EmailStr
from typing import Literal
class Employee(BaseModel):
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: Literal["WFO","WFO"]
class EmployeeResponse(Employee):
    id:int
    is_active: bool =True
    created_at: str