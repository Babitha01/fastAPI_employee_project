from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse
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

@app.post("/employees", response_model=EmployeeResponse)
def add_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    existing_employee = db.query(Employee).filter(
        Employee.email == employee.email
    ).first()
    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    return service.create_employee(db, employee)

@app.get("/employees",response_model=list[EmployeeResponse]) 
def get_employees(db: Session = Depends(get_db)):
    return service.get_all_employees(db)

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
    employee = service.get_employee_by_id(db, employee_id)
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
        Employee.email == employee.email,
        Employee.id != employee_id
    ).first()
    if duplicate_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    updated_employee = service.update_employee(
        db, employee_id, employee
    )
    return updated_employee

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
    deleted_employee = service.delete_employee(db, employee_id)
    if deleted_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )
    return {
        "message": "Employee deleted successfully",
        "employee": deleted_employee
    }