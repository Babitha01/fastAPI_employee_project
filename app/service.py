from datetime import datetime
employees = []
next_employee_id = 1
def create_employee(employee):
    global next_employee_id
    employee_id = next_employee_id
    next_employee_id +=1
    
    employee_data = {
        "id": employee_id,
        "name": employee.name,
        "email": employee.email,
        "department": employee.department,
        "primary_skill": employee.primary_skill,
        "location": employee.location,
        "work_mode": employee.work_mode,
        "is_active": True,
        "created_at": datetime.now().isoformat()
    }
    employees.append(employee_data)
    return employee_data
def get_all_employees():
    return employees
def get_employee_by_id(employee_id):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee
    return None
def update_employee(employee_id, employee):
    for index, existing_employee in enumerate(employees):
        if existing_employee["id"] == employee_id:
            updated_employee = {
                "id": employee_id,
                "name": employee.name,
                "email": employee.email,
                "department": employee.department,
                "primary_skill": employee.primary_skill,
                "location": employee.location,
                "work_mode": employee.work_mode,
                "is_active": existing_employee["is_active"],
                "created_at": existing_employee["created_at"]
            }
            employees[index] = updated_employee
            return updated_employee
    return None
def delete_employee(employee_id):
    for index, employee in enumerate(employees):
        if employee["id"] == employee_id:
            deleted_employee = employees.pop(index)
            return deleted_employee
    return None