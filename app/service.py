from sqlalchemy.orm import Session
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeUpdate
def create_employee(db: Session, employee: EmployeeCreate):
    new_employee = Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department,
        primary_skill=employee.primary_skill,
        location=employee.location,
        work_mode=employee.work_mode,
        is_active=True
    )
    try:
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)

        return new_employee
    except Exception:
        db.rollback()
        raise

def get_all_employees(db: Session):
    return db.query(Employee).all()

def get_employee_by_id(db: Session, employee_id: int):
    return db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

def update_employee(
    db: Session,
    employee_id: int,
    employee: EmployeeUpdate
):
    existing_employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()
    if existing_employee is None:
        return None
    existing_employee.name = employee.name
    existing_employee.email = employee.email
    existing_employee.department = employee.department
    existing_employee.primary_skill = employee.primary_skill
    existing_employee.location = employee.location
    existing_employee.work_mode = employee.work_mode
    try:
        db.commit()
        db.refresh(existing_employee)

        return existing_employee
    except Exception:
        db.rollback()
        raise

def delete_employee(db: Session, employee_id: int):
    existing_employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()
    if existing_employee is None:
        return None
    try:
        db.delete(existing_employee)
        db.commit()
        return existing_employee
    except Exception:
        db.rollback()
        raise