from sqlalchemy.orm import Session
from .models import Employee
from .schemas import EmployeeCreate

def create_employee(db: Session, employee_data: EmployeeCreate):
    email = employee_data.email.lower()
    existing_employee = (
        db.query(Employee)
        .filter(Employee.email.ilike(email)).first()
    )
    if existing_employee:
        return None
    employee = Employee(
        name=employee_data.name,
        email=email,
        department=employee_data.department,
        primary_skill=employee_data.primary_skill,
        location=employee_data.location,
        work_mode=employee_data.work_mode,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

def get_all_employees(db: Session):
    return db.query(Employee).order_by(Employee.id).all()

def get_employee_by_id(db: Session, employee_id: int):
    return (
        db.query(Employee)
        .filter(Employee.id == employee_id).first()
    )