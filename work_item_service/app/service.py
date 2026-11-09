import httpx
from sqlalchemy.orm import Session
from .models import WorkItem
from .schemas import WorkItemCreate

import os
EMPLOYEE_SERVICE_URL = os.getenv(
    "EMPLOYEE_SERVICE_URL",
    "http://localhost:8001"
)

def verify_employee(employee_id: int):
    url = f"{EMPLOYEE_SERVICE_URL}/employees/{employee_id}"
    try:
        response = httpx.get(url, timeout=5.0)
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True
    except httpx.HTTPError:
        raise ConnectionError("Employee Service is unavailable")

def create_work_item(db: Session, work_item_data: WorkItemCreate):
    employee_exists = verify_employee(work_item_data.employee_id)
    if not employee_exists:
        return None
    work_item = WorkItem(
        title=work_item_data.title,
        description=work_item_data.description,
        employee_id=work_item_data.employee_id,
        status=work_item_data.status,
        priority=work_item_data.priority,
        due_date=work_item_data.due_date,
    )
    db.add(work_item)
    db.commit()
    db.refresh(work_item)
    return work_item

def get_all_work_items(db: Session):
    return db.query(WorkItem).order_by(WorkItem.id).all()

def get_work_item_by_id(db: Session, work_item_id: int):
    return db.query(WorkItem).filter(
        WorkItem.id == work_item_id
    ).first()