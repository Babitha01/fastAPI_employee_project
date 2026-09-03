from fastapi import FastAPI, HTTPException,Path
from app.schemas import Employee, EmployeeResponse
from datetime import datetime

app = FastAPI()

employees = []
next_id = 1


@app.get("/health")
def health_check():
    return {"status": "Application is running"}


@app.post("/employees", response_model=EmployeeResponse)
def create_employee(employee: Employee):
    global next_id
    for existing_expolyee in employees:
        if existing_expolyee.email == employee.email:
            raise HTTPException(status_code=400,detail="Email already exists")

    new_employee = EmployeeResponse(
        id=next_id,
        name=employee.name,
        email=employee.email,
        department=employee.department,
        primary_skill=employee.primary_skill,
        location=employee.location,
        work_mode=employee.work_mode,
        is_active=True,
        created_at=datetime.now().isoformat()
    )

    employees.append(new_employee)
    next_id += 1

    return new_employee


@app.get("/employees")
def get_employees():
    return employees


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int=Path(..., gt=0)):
    for employee in employees:
        if employee.id == employee_id:
            return employee

    raise HTTPException(status_code=404, detail="Employee not found")


@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int = Path(..., gt=0),
    employee: Employee = None
):
    for index, existing_employee in enumerate(employees):

        if existing_employee.id == employee_id:

            for other_employee in employees:
                if (
                    other_employee.id != employee_id
                    and other_employee.email == employee.email
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="Email already exists"
                    )

            updated_employee = EmployeeResponse(
                id=employee_id,
                name=employee.name,
                email=employee.email,
                department=employee.department,
                primary_skill=employee.primary_skill,
                location=employee.location,
                work_mode=employee.work_mode,
                is_active=existing_employee.is_active,
                created_at=existing_employee.created_at
            )

            employees[index] = updated_employee

            return updated_employee

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    for index, employee in enumerate(employees):
        if employee.id == employee_id:
            deleted_employee = employees.pop(index)
            return {
                "message": "Employee deleted successfully",
                "employee": deleted_employee
            }

    raise HTTPException(status_code=404, detail="Employee not found")