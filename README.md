# FastAPI Employee Management

# Project Description

This project is a FastAPI backend for managing employee records and work items.
Employee and work item records are stored in a MySQL database using SQLAlchemy. The records remain available even after the application is restarted.

## Technologies Used

* Python 3.12
* FastAPI
* Pydantic
* MySQL
* SQLAlchemy
* PyMySQL
* Uvicorn
* Swagger UI
* Git

## Employee Fields

* ID
* Name
* Email
* Department
* Primary Skill
* Location
* Work Mode
* Is Active
* Created At

## Employee APIs

* POST /employees
* GET /employees
* GET /employees/{id}
* PUT /employees/{id}
* DELETE /employees/{id}
* GET /health

## Employee Validation

* Required employee fields are validated.
* Empty or whitespace-only required fields are rejected.
* Email format is validated.
* Duplicate email is not allowed.
* Email uniqueness is checked without treating uppercase and lowercase as different.
* Work mode accepts WFH or WFO.
* Employee ID must be greater than 0.
* 404 error is returned when an employee is not found.
* Employee IDs are generated automatically by the database.
* "is_active" is set to "true" by default.
* "created_at" is generated when an employee is created and preserved during updates.
* Failed database changes are rolled back so that later requests can continue working.

## Task 3 - Search, Filtering and Pagination

The `GET /employees` endpoint supports searching, filtering and pagination.

### Query Parameters

* `search` - Searches employees by name using partial and case-insensitive matching.
* `department` - Filters employees by department.
* `work_mode` - Filters employees by WFH or WFO.
* `is_active` - Filters employees by active or inactive status.
* `limit` - Maximum number of records to return. Default is 10. Allowed values are 1 to 100.
* `offset` - Number of records to skip. Default is 0. Negative values are not allowed.

### Example Request

GET /employees?department=Engineering&work_mode=WFH&limit=5&offset=0

### Response Format

The `GET /employees` endpoint returns:

{
  "total": 2,
  "limit": 10,
  "offset": 0,
  "items": []
}

total - Number of matching employees before pagination.
limit - Requested page size.
offset - Number of records skipped.
items - List of matching employee records.

# Task 3 Testing

The following scenarios were tested using Swagger UI:

* Employee name search
* Department filtering
* Work mode filtering
* Active/inactive filtering
* Combined filters
* Partial name search
* Pagination using limit and offset
* No matching results
* Offset greater than the matching records
* Invalid limit values
* Negative offset validation
* Invalid work mode validation

Search, filtering and pagination are performed using SQLAlchemy queries.

# Task 4 - Work Item Management

Task 4 adds work item management to the Employee Management API.
Each work item is assigned to an existing employee using a foreign key relationship.

# Work Item Fields
* ID
* Title
* Description
* Employee ID
* Status
* Priority
* Due Date
* Created At
* Assigned Employee

# Work Item Status
* TODO
* IN_PROGRESS
* COMPLETED

# Work Item Priority
* LOW
* MEDIUM
* HIGH

# Work Item APIs
* POST /work-items
* GET /work-items
* GET /work-items/{work_item_id}
* PUT /work-items/{work_item_id}
* DELETE /work-items/{work_item_id}

Task 4 Query Parameters

The GET /work-items endpoint supports search, filtering and pagination.

* search - Searches work items by title using partial and case-insensitive matching.
* employee_id - Filters work items by assigned employee.
* status - Filters work items by status.
* priority - Filters work items by priority.
* limit - Maximum number of records to return. Default is 10. Allowed values are 1 to 100.
* offset - Number of records to skip. Default is 0. Negative values are not allowed.

# Example Request

GET /work-items?
employee_id=2&status=TODO&priority=MEDIUM&limit=10&offset=0

# Work Item Response

Each work item response includes the assigned employee details.

{
  "id": 1,
  "title": "Prepare weekly report",
  "description": "Weekly status report",
  "employee_id": 2,
  "status": "TODO",
  "priority": "MEDIUM",
  "due_date": "2026-10-05",
  "created_at": "2026-10-05T10:00:00",
  "assigned_employee": {
    "id": 2,
    "name": "Babitha",
    "email": "Babitha1@example.com"
  }
}

# Work Item List Response

The GET /work-items endpoint returns:

{
  "total": 4,
  "limit": 10,
  "offset": 0,
  "items": []
}

* total - Number of matching work items before pagination.
* limit - Requested page size.
* offset - Number of records skipped.
* items - List of matching work items.

# Work Item Validation

* Title is required.
* Empty or whitespace-only titles are rejected.
* Employee ID must be greater than 0.
* Assigned employee must exist.
* Status accepts TODO, IN_PROGRESS or COMPLETED.
* Priority accepts LOW, MEDIUM or HIGH.
* Work item ID must be greater than 0.
* 404 error is returned when a work item or employee is not found.
* Database changes are rolled back when a database error occurs.

# Employee and Work Item Relationship

A work item belongs to an employee through the employee_id foreign key.

The SQLAlchemy relationship connects the Employee and WorkItem models.

Each work item response also returns the assigned employee's:

* ID
* Name
* Email

# Task 4 Testing

The following scenarios were tested using Swagger UI:

* Create work item
* Create work item with non-existing employee
* Get work item by ID
* Search by title
* Filter by employee ID
* Filter by status
* Filter by priority
* Combined filters
* Pagination using limit and offset
* Update work item
* Reassign work item to another employee
* Invalid status validation
* Invalid priority validation
* Blank title validation
* Delete work item
* Verify deleted work item returns 404
* Verify data remains available after application restart
* Verify existing employee APIs continue working

Search, filtering, pagination and ordering are performed using SQLAlchemy queries.

# Database Setup

Create a MySQL database named employee_db.

The application uses SQLAlchemy and PyMySQL to connect to MySQL and perform create, read and delete operations.

The employees and work_items tables are created using the SQLAlchemy models when the application starts.

The email field has a database-level unique constraint.

The work_items.employee_id field is a foreign key that references the employees.id field.

Database sessions are closed after use.

# Database Configuration

Create a local .env file in the project root and add the database connection details.

DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=employee_db

A .env.example file is also included with placeholder values for reference.

Do not commit the .env file or database passwords to GitHub.

# How to Run

Create and activate a virtual environment.

Install dependencies:

pip install -r requirements.txt

# Start the application:

uvicorn app.main:app --reload

Open Swagger UI:

http://127.0.0.1:8000/docs

# What I Learned

I learned how to connect a FastAPI application to a MySQL database using SQLAlchemy. I also learned how to use database models, sessions, CRUD operations, validations, database transactions, and test API responses using Swagger UI.

In Task 3, I learned how to implement search, filtering and pagination using SQLAlchemy queries. I also learned how query parameters work in FastAPI and how to validate values such as limit, offset and work mode.

In Task 4, I learned how to create a WorkItem model and connect it with the Employee model using a foreign key and SQLAlchemy relationship. I also learned how to implement work item CRUD operations, filtering, combined filters, pagination, validation and assigned employee details in API responses.

# Difficulties

I faced difficulties while setting up the MySQL connection, configuring the database connection details, handling duplicate email validation, and understanding SQLAlchemy database operations. I also faced some issues while testing the APIs using Swagger UI.

During Task 3, I faced some difficulties while implementing the pagination response structure, combining multiple filters, and testing different query parameter combinations.

During Task 4, I faced some difficulties while implementing the Employee and WorkItem relationship, handling the assigned employee response, testing combined filters and pagination, and validating invalid status, priority and employee values.

# Assumptions

Employee and work item records are stored in the MySQL database and remain available after application restarts.

Database credentials are stored locally in the .env file and are not committed to the repository.

Fictional employee and work item data is used for testing.