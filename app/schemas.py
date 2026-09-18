from pydantic import BaseModel, EmailStr, Field ,field_validator
from typing import Literal
from datetime import datetime
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
class Config:
    from_attributes = True