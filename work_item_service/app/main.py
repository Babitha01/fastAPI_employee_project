from fastapi import FastAPI, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models, schemas, service

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Work Item Service")

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
    "/work-items",
    response_model=schemas.WorkItemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_work_item(
    work_item_data: schemas.WorkItemCreate,
    db: Session = Depends(get_db)
):
    try:
        work_item = service.create_work_item(db, work_item_data)
        if work_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )
        return work_item
    except ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Employee Service is unavailable"
        )

@app.get(
    "/work-items",
    response_model=list[schemas.WorkItemResponse]
)
def get_all_work_items(db: Session = Depends(get_db)):
    return service.get_all_work_items(db)

@app.get(
    "/work-items/{work_item_id}",
    response_model=schemas.WorkItemResponse
)
def get_work_item(
    work_item_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    work_item = service.get_work_item_by_id(db, work_item_id)
    if work_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work item not found"
        )
    return work_item