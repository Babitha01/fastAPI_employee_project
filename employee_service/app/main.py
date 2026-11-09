from fastapi import FastAPI, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models, schemas, service
models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Employee Service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post(
    "/employees",
    response_model=schemas.EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    employee_data: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
):
    employee = service.create_employee(db, employee_data)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee email already exists",
        )
    return employee

@app.get(
    "/employees",
    response_model=list[schemas.EmployeeResponse],
)
def get_all_employees(db: Session = Depends(get_db)):
    return service.get_all_employees(db)

@app.get(
    "/employees/{employee_id}",
    response_model=schemas.EmployeeResponse,
)
def get_employee(
    employee_id: int = Path(gt=0),
    db: Session = Depends(get_db),
):
    employee = service.get_employee_by_id(db, employee_id)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return employee