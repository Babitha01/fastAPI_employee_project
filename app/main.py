from fastapi import FastAPI, HTTPException, Depends, Query 
from typing import Literal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse,EmployeeListResponse
from app import service
from app.database import engine, Base
from app.models import Employee
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()
Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "Application is running"}

@app.post("/employees", response_model=EmployeeResponse,status_code=201)
def add_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    existing_employee = db.query(Employee).filter(
        func.lower(Employee.email) == employee.email.lower()).first()
    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    try:
       return service.create_employee(db, employee)
    except SQLAlchemyError:
        raise HTTPException(status_code=500,detail="Database operation failed. Please try again.")        
    
@app.get("/employees", response_model=EmployeeListResponse)
def get_employees(
    department: str | None = Query(default=None),
    work_mode: Literal["WFH","WFO"] | None=Query(default=None),
    is_active: bool | None = Query(default=None),
    search: str | None =Query(default=None),
    limit: int=Query(default=10,ge=1,le=100),
    offset: int =Query(default=0,ge=0),
    db: Session = Depends(get_db)
):
    try:
        return service.get_all_employees(db,department,search,work_mode,is_active,limit,offset)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed. Please try again."
        )
        
@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    if employee_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Employee ID must be greater than 0"
        )
    try:    
        employee = service.get_employee_by_id(db, employee_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500,detail="Databse operation failed. Please try again.")
    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )
    return employee

@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    if employee_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Employee ID must be greater than 0"
        )
    existing_employee = service.get_employee_by_id(db, employee_id)
    if existing_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )
    duplicate_email = db.query(Employee).filter(
        func.lower(Employee.email)== employee.email.lower(),
        Employee.id != employee_id).first()
    if duplicate_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    try:
        updated_employee = service.update_employee(
        db, employee_id, employee
    )
        return updated_employee
    except SQLAlchemyError:
        raise HTTPException(status_code=500,detail="Database operation failed. Please try again.")
    
@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    if employee_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Employee ID must be greater than 0"
        )
    try:
        deleted_employee = service.delete_employee(db, employee_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500,detail="Database operation failed. Please try again.")
    if deleted_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )
    return {
        "message": f"Employee with ID {employee_id} was deleted successfully"
    }