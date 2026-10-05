from pydantic import BaseModel, EmailStr, Field ,field_validator
from typing import Literal
from datetime import datetime , date
class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    department: str = Field(min_length=1)
    primary_skill: str = Field(min_length=1)
    location: str = Field(min_length=1)
    work_mode: Literal["WFH", "WFO"]
    
    @field_validator("name","department","primary_skill","location")
    @classmethod
    def reject_space_only(cls,value):
        if not value.strip():
            raise ValueError("Field cannot be empty or contain only spaces")
        return value
    
class EmployeeUpdate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    department: str = Field(min_length=1)
    primary_skill: str = Field(min_length=1)
    location: str = Field(min_length=1)
    work_mode: Literal["WFH", "WFO"]
    is_active: bool
    
    @field_validator("name","department","primary_skill","location")
    @classmethod
    def reject_space_only(cls,value):
            if not value.strip():
                raise ValueError("Field cannot be empty or contain only spaces")
            return value
        
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
    
class EmployeeListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[EmployeeResponse]
        
class Config:
    from_attributes = True
    
class AssignedEmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    class Config:
        from_attributes = True

class WorkItemCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str | None = None
    employee_id: int = Field(gt=0)
    status: Literal["TODO", "IN_PROGRESS", "COMPLETED"] = "TODO"
    priority: Literal["LOW", "MEDIUM", "HIGH"] = "MEDIUM"
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def reject_blank_title(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty or contain only spaces")
        return value

class WorkItemUpdate(BaseModel):
    title: str = Field(min_length=1)
    description: str | None = None
    employee_id: int = Field(gt=0)
    status: Literal["TODO", "IN_PROGRESS", "COMPLETED"]
    priority: Literal["LOW", "MEDIUM", "HIGH"]
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def reject_blank_title(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty or contain only spaces")
        return value

class WorkItemResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    employee_id: int
    status: Literal["TODO", "IN_PROGRESS", "COMPLETED"]
    priority: Literal["LOW", "MEDIUM", "HIGH"]
    due_date: date | None = None
    created_at: datetime
    assigned_employee: AssignedEmployeeResponse
    class Config:
        from_attributes = True

class WorkItemListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[WorkItemResponse]
    class Config:
        from_attributes = True