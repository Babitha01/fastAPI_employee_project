from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from app.models import Employee,WorkItem
from app.schemas import EmployeeCreate, EmployeeUpdate,WorkItemCreate,WorkItemUpdate

class WorkItemStatusError(Exception):
    pass

def change_work_item_status(existing_work_item, new_status):
    current_status = existing_work_item.status
    if new_status == current_status:
        return
    if current_status == "TODO" and new_status == "IN_PROGRESS":
        existing_work_item.status = new_status
    elif current_status == "IN_PROGRESS" and new_status == "COMPLETED":
        existing_work_item.status = new_status
    else:
        raise WorkItemStatusError(
            f"Invalid status transition from {current_status} to {new_status}"
        )
        
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
    
def create_work_item(db: Session, work_item: WorkItemCreate):
    new_work_item = WorkItem(
        title=work_item.title,
        description=work_item.description,
        employee_id=work_item.employee_id,
        status=work_item.status,
        priority=work_item.priority,
        due_date=work_item.due_date
    )

    try:
        db.add(new_work_item)
        db.commit()
        db.refresh(new_work_item)
        return new_work_item
    except SQLAlchemyError:
        db.rollback()
        raise


def get_all_work_items(
    db: Session,
    search=None,
    employee_id=None,
    status=None,
    priority=None,
    limit=10,
    offset=0
):
    query = db.query(WorkItem)
    if search:
        query = query.filter(WorkItem.title.ilike(f"%{search}%"))
    if employee_id is not None:
        query = query.filter(WorkItem.employee_id == employee_id)
    if status:
        query = query.filter(WorkItem.status == status)
    if priority:
        query = query.filter(WorkItem.priority == priority)
    total = query.count()
    items = (
        query
        .order_by(WorkItem.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items
    }
    
def get_work_item_by_id(db: Session, work_item_id: int):
    return (
        db.query(WorkItem)
        .filter(WorkItem.id == work_item_id)
        .first()
    )

def update_work_item(
    db: Session,
    work_item_id: int,
    work_item: WorkItemUpdate
):
    existing_work_item = (
        db.query(WorkItem)
        .filter(WorkItem.id == work_item_id)
        .first()
    )
    if existing_work_item is None:
        return None
    if "status" in work_item.model_fields_set:
        if work_item.status is None:
            raise WorkItemStatusError("Status cannot be null")
        change_work_item_status(
            existing_work_item,
            work_item.status
        )
    existing_work_item.title = work_item.title
    existing_work_item.description = work_item.description
    existing_work_item.employee_id = work_item.employee_id
    existing_work_item.priority = work_item.priority
    existing_work_item.due_date = work_item.due_date
    try:
        db.commit()
        db.refresh(existing_work_item)
        return existing_work_item
    except SQLAlchemyError:
        db.rollback()
        raise
    
def delete_work_item(db: Session, work_item_id: int):
    existing_work_item = (
        db.query(WorkItem)
        .filter(WorkItem.id == work_item_id)
        .first()
    )

    if existing_work_item is None:
        return None
    try:
        db.delete(existing_work_item)
        db.commit()
        return existing_work_item
    except SQLAlchemyError:
        db.rollback()
        raise
    
def update_work_item_status(
    db: Session,
    work_item_id: int,
    new_status: str
):
    existing_work_item = (
        db.query(WorkItem)
        .filter(WorkItem.id == work_item_id)
        .first()
    )
    if existing_work_item is None:
        return None
    change_work_item_status(existing_work_item, new_status)
    try:
        db.commit()
        db.refresh(existing_work_item)
        return existing_work_item
    except SQLAlchemyError:
        db.rollback()
        raise

def get_employee_work_summary(
    db: Session,
    employee_id: int
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )
    if employee is None:
        return None
    status_counts = (
        db.query(WorkItem.status, func.count(WorkItem.id))
        .filter(WorkItem.employee_id == employee_id)
        .group_by(WorkItem.status)
        .all()
    )
    summary = {
        "employee_id": employee_id,
        "total_work_items": 0,
        "todo": 0,
        "in_progress": 0,
        "completed": 0
    }
    for status, count in status_counts:
        if status == "TODO":
            summary["todo"] = count
        elif status == "IN_PROGRESS":
            summary["in_progress"] = count
        elif status == "COMPLETED":
            summary["completed"] = count
        summary["total_work_items"] += count
    return summary    
