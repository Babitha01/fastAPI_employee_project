from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
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
    except SQLAlchemyError:
        db.rollback()
        raise 

def get_all_employees(db: Session, department=None,search=None, work_mode=None,is_active=None,limit=10,offset=0):
    query = db.query(Employee)
    if department:
        query = query.filter(Employee.department == department)
    if search:
        query=query.filter(Employee.name.ilike(f"%{search}%"))
    if work_mode:
        query = query.filter(Employee.work_mode == work_mode)
    if is_active is not None:
        query=query.filter(Employee.is_active==is_active)
    total =query.count()
    items=query.order_by(Employee.id.asc()).offset(offset).limit(limit).all()
    return {
        "total":total,
        "limit":limit,
        "offset":offset,
        "items":items
    }
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
    existing_employee.is_active = employee.is_active
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