# Employee Management FastAPI

## Project Description

This project is a FastAPI backend for managing employee records.

Employee records are temporarily stored in a Python list.

## Technologies Used

- Python 3.12
- FastAPI
- Pydantic
- Uvicorn
- Swagger UI

## Employee Fields

- ID
- Name
- Email
- Department
- Primary Skill
- Location
- Work Mode
- Is Active
- Created At

## APIs

- POST /employees
- GET /employees
- GET /employees/{id}
- PUT /employees/{id}
- DELETE /employees/{id}
- GET /health

## Validation

- Required employee fields are validated.
- Email format is validated.
- Duplicate email is not allowed.
- Work mode accepts WFH or WFO.
- Employee ID must be greater than 0.
- 404 error is returned when an employee is not found.

## How to Run

Create and activate a virtual environment.

Install dependencies:

```bash
pip install -r requirements.txt

Start the application:

uvicorn app.main:app --reload

Open Swagger UI:
http://127.0.0.1:8000/docs

What I Learned
I learned how to build a REST API using FastAPI, create Pydantic schemas, implement CRUD operations, add validations, and test APIs using Swagger UI.

Difficulties
I faced difficulties with employee ID validation, duplicate email validation, and understanding FastAPI while developing the project.

Assumptions
Employee data is stored temporarily in a Python list. The data will be lost when the application restarts.