from fastapi import FastAPI, HTTPException, Depends, Query 
from typing import Literal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse,EmployeeListResponse,WorkItemCreate,WorkItemUpdate,WorkItemResponse,WorkItemListResponse
from app import service
from app.database import engine, Base
from app.models import Employee ,WorkItem

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

@app.post(
    "/work-items",
    response_model=WorkItemResponse,
    status_code=201
)
def add_work_item(
    work_item: WorkItemCreate,
    db: Session = Depends(get_db)
):
    employee = service.get_employee_by_id(db, work_item.employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    try:
        return service.create_work_item(db, work_item)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed. Please try again."
        )

@app.get(
    "/work-items",
    response_model=WorkItemListResponse
)
def get_work_items(
    search: str | None = Query(default=None),
    employee_id: int | None = Query(default=None, gt=0),
    status: Literal["TODO", "IN_PROGRESS", "COMPLETED"] | None = Query(default=None),
    priority: Literal["LOW", "MEDIUM", "HIGH"] | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    try:
        return service.get_all_work_items(
            db,
            search,
            employee_id,
            status,
            priority,
            limit,
            offset
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed. Please try again."
        )

@app.get(
    "/work-items/{work_item_id}",
    response_model=WorkItemResponse
)
def get_work_item(
    work_item_id: int,
    db: Session = Depends(get_db)
):
    if work_item_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Work item ID must be greater than 0"
        )
    try:
        work_item = service.get_work_item_by_id(
            db,
            work_item_id
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed. Please try again."
        )
    if work_item is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found"
        )
    return work_item

@app.put(
    "/work-items/{work_item_id}",
    response_model=WorkItemResponse
)
def update_work_item(
    work_item_id: int,
    work_item: WorkItemUpdate,
    db: Session = Depends(get_db)
):
    if work_item_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Work item ID must be greater than 0"
        )
    existing_work_item = service.get_work_item_by_id(
        db,
        work_item_id
    )
    if existing_work_item is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found"
        )
    employee = service.get_employee_by_id(
        db,
        work_item.employee_id
    )
    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )
    try:
        return service.update_work_item(
            db,
            work_item_id,
            work_item
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed. Please try again."
        )

@app.delete(
    "/work-items/{work_item_id}",
    status_code=204
)
def delete_work_item(
    work_item_id: int,
    db: Session = Depends(get_db)
):
    if work_item_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Work item ID must be greater than 0"
        )
    try:
        deleted_work_item = service.delete_work_item(
            db,
            work_item_id
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed. Please try again."
        )
    if deleted_work_item is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found"
        )
    return None
