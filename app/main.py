from fastapi import FastAPI,HTTPException
from app.schemas import EmployeeCreate,EmployeeUpdate,EmployeeResponse
from app import service
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "Application is running"}

@app.post("/employees", response_model=EmployeeResponse)
def add_employee(employee: EmployeeCreate):
    for existing_employee in service.employees:
        if existing_employee["email"] == employee.email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )
    return service.create_employee(employee)

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int):
    if employee_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Employee ID must be greater than 0"
        )

    employee = service.get_employee_by_id(employee_id)
    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )
    return employee

@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee: EmployeeUpdate):
    if employee_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Employee ID must be greater than 0"
        )
    updated_employee = service.update_employee(employee_id, employee)
    if updated_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )
    return updated_employee

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    if employee_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Employee ID must be greater than 0"
        )
    deleted_employee = service.delete_employee(employee_id)
    if deleted_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )
    return {
        "message": "Employee deleted successfully",
        "employee": deleted_employee
    }