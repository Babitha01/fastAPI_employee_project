# FastAPI Employee Management

## Project Description

This project is a FastAPI backend for managing employee records and work items. Employee and work item records are stored in a MySQL database using SQLAlchemy. The records remain available even after the application is restarted.

## Technologies Used

- Python
- FastAPI
- Pydantic
- MySQL
- SQLAlchemy
- PyMySQL
- Uvicorn
- Swagger UI
- Git and GitHub

## Setup Instructions

### Clone the Repository

git clone https://github.com/Babitha01/fastAPI_employee_project.git
cd fastAPI_employee_project
git checkout task-5

### Create and Activate a Virtual Environment

python -m venv venv

For Windows:

venv\Scripts\activate

### Install Dependencies

pip install -r requirements.txt

### Database Configuration

Create a MySQL database named `employee_db`.

Create a local `.env` file in the project root and configure the database connection:

DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=employee_db

Replace the placeholder values with your local MySQL credentials. Do not commit `.env` or database passwords to GitHub. A `.env.example` file is included for reference.

### Start the Application

Ensure the MySQL server is running, then execute:

uvicorn app.main:app --reload

Open Swagger UI:

http://127.0.0.1:8000/docs

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

## Employee APIs

- `POST /employees`
- `GET /employees`
- `GET /employees/{id}`
- `PUT /employees/{id}`
- `DELETE /employees/{id}`
- `GET /health`

## Employee Validation

- Required employee fields are validated.
- Empty or whitespace-only required fields are rejected.
- Email format is validated.
- Duplicate email is not allowed.
- Email uniqueness is checked without treating uppercase and lowercase as different.
- Work mode accepts `WFH` or `WFO`.
- Employee ID must be greater than 0.
- A 404 error is returned when an employee is not found.
- Employee IDs are generated automatically by the database.
- `is_active` is set to `true` by default.
- `created_at` is generated when an employee is created and preserved during updates.
- Failed database changes are rolled back so that later requests can continue working.

## Task 3 - Search, Filtering and Pagination

The `GET /employees` endpoint supports searching, filtering and pagination.

### Query Parameters

- `search` - Searches employees by name using partial and case-insensitive matching.
- `department` - Filters employees by department.
- `work_mode` - Filters employees by WFH or WFO.
- `is_active` - Filters employees by active or inactive status.
- `limit` - Maximum number of records to return. Default is 10. Allowed values are 1 to 100.
- `offset` - Number of records to skip. Default is 0. Negative values are not allowed.

### Example Request

GET /employees?department=Engineering&work_mode=WFH&limit=5&offset=0

### Response Format

The `GET /employees` endpoint returns a paginated response:

{
  "total": 2,
  "limit": 10,
  "offset": 0,
  "items": []
}

- `total` - Number of matching employees before pagination.
- `limit` - Requested page size.
- `offset` - Number of records skipped.
- `items` - List of matching employee records.

### Task 3 Testing

The following scenarios were tested using Swagger UI:

- Employee name search
- Department filtering
- Work mode filtering
- Active/inactive filtering
- Combined filters
- Partial name search
- Pagination using limit and offset
- No matching results
- Offset greater than the matching records
- Invalid limit values
- Negative offset validation
- Invalid work mode validation

Search, filtering and pagination are performed using SQLAlchemy queries.

## Task 4 - Work Item Management

Task 4 adds work item management to the Employee Management API. Each work item is assigned to an existing employee using a foreign key relationship.

### Work Item Fields

- ID
- Title
- Description
- Employee ID
- Status
- Priority
- Due Date
- Created At
- Assigned Employee

### Work Item Status

- `TODO`
- `IN_PROGRESS`
- `COMPLETED`

### Work Item Priority

- `LOW`
- `MEDIUM`
- `HIGH`

### Work Item APIs

- `POST /work-items`
- `GET /work-items`
- `GET /work-items/{work_item_id}`
- `PUT /work-items/{work_item_id}`
- `DELETE /work-items/{work_item_id}`

### Task 4 Query Parameters

The `GET /work-items` endpoint supports search, filtering and pagination.

- `search` - Searches work items by title using partial and case-insensitive matching.
- `employee_id` - Filters work items by assigned employee.
- `status` - Filters work items by status.
- `priority` - Filters work items by priority.
- `limit` - Maximum number of records to return. Default is 10. Allowed values are 1 to 100.
- `offset` - Number of records to skip. Default is 0. Negative values are not allowed.

### Example Request

GET /work-items?employee_id=2&status=TODO&priority=MEDIUM&limit=10&offset=0

### Work Item Response

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

### Work Item List Response

The `GET /work-items` endpoint returns:

{
  "total": 4,
  "limit": 10,
  "offset": 0,
  "items": []
}

- `total` - Number of matching work items before pagination.
- `limit` - Requested page size.
- `offset` - Number of records skipped.
- `items` - List of matching work items.

### Work Item Validation

- Title is required.
- Empty or whitespace-only titles are rejected.
- Employee ID must be greater than 0.
- Assigned employee must exist.
- Status accepts `TODO`, `IN_PROGRESS` or `COMPLETED`.
- Priority accepts `LOW`, `MEDIUM` or `HIGH`.
- Work item ID must be greater than 0.
- A 404 error is returned when a work item or employee is not found.
- Database changes are rolled back when a database error occurs.

### Employee and Work Item Relationship

A work item belongs to an employee through the `employee_id` foreign key.

The SQLAlchemy relationship connects the Employee and WorkItem models. Each work item response also returns the assigned employee's ID, name and email.

### Task 4 Testing

The following scenarios were tested using Swagger UI:

- Create work item
- Create work item with non-existing employee
- Get work item by ID
- Search by title
- Filter by employee ID
- Filter by status
- Filter by priority
- Combined filters
- Pagination using limit and offset
- Update work item
- Reassign work item to another employee
- Invalid status validation
- Invalid priority validation
- Blank title validation
- Delete work item
- Verify deleted work item returns 404
- Verify data remains available after application restart
- Verify existing employee APIs continue working

Search, filtering, pagination and ordering are performed using SQLAlchemy queries.

## Task 5 - Work Item Status Transitions and Employee Work Summary

Task 5 adds controlled work item status transitions and an employee work summary endpoint.

### Work Item Status Transition Rules

Allowed status transitions:

- `TODO` → `IN_PROGRESS`
- `IN_PROGRESS` → `COMPLETED`

Rules:

- New work items must start with `TODO`.
- The same status can be submitted without changing the status.
- Skipped or backward status transitions are rejected with HTTP 400.
- Invalid status values are rejected with HTTP 422.
- A missing or explicitly null status in the PATCH request is rejected with HTTP 422.
- In a PUT request, omitting the status preserves the existing status.
- In a PUT request, explicitly sending `status: null` is rejected with HTTP 422.
- If a PUT request contains an invalid status transition, the update is rejected without saving other field changes.
- A 404 error is returned when the work item does not exist.

### Update Work Item Status API

**Endpoint:**

PATCH /work-items/{work_item_id}/status

Example request:

{
  "status": "IN_PROGRESS"
}

Example response:

{
  "id": 1,
  "status": "IN_PROGRESS"
}

The endpoint validates status transitions and updates the work item status only when the transition is allowed.

### Employee Work Summary API

**Endpoint:**

```text
GET /employees/{employee_id}/work-summary
```

This endpoint returns the work item counts for the specified employee.

Example response:

{
  "employee_id": 6,
  "total_work_items": 2,
  "todo": 2,
  "in_progress": 0,
  "completed": 0
}

The response contains:

- `employee_id` - ID of the employee.
- `total_work_items` - Total work items currently assigned to the employee.
- `todo` - Number of work items with `TODO` status.
- `in_progress` - Number of work items with `IN_PROGRESS` status.
- `completed` - Number of work items with `COMPLETED` status.

The total count equals the sum of the three status counts. Employees with no assigned work items return zero counts. Reassignment updates the summaries of the relevant employees, and deleted work items are excluded from the counts.

A 404 error is returned when the employee does not exist.

### Task 5 Testing

The following scenarios were tested using Swagger UI:

- Valid `TODO` to `IN_PROGRESS` transition
- Valid `IN_PROGRESS` to `COMPLETED` transition
- Submitting the same status
- Rejecting invalid status values
- Rejecting missing and null status in PATCH requests
- Rejecting skipped or backward status transitions
- Creating a work item with a non-`TODO` status
- Updating a work item using PUT without a status field
- Rejecting a PUT request with `status: null` with HTTP 422
- Verifying that a rejected PUT request does not modify other fields
- Handling missing work items and employees
- Retrieving employee work summary counts
- Reassigning a work item and checking employee summaries
- Deleting a work item and checking that it is excluded from the list
- Verifying database persistence after restarting the application

### Task 5 Screenshots

Screenshots of the Task 5 API responses and validation results are available in the repository's screenshots section.

- Status update
- Invalid status transition
- Invalid status validation
- Work item creation validation
- Employee work summary
- Employee not found validation
- PUT request with null status returning HTTP 422

## Database Setup

Create a MySQL database named `employee_db`.

The application uses SQLAlchemy and PyMySQL to connect to MySQL and perform database operations. The employees and work_items tables are created using the SQLAlchemy models when the application starts.

- The email field has a database-level unique constraint.
- The `work_items.employee_id` field is a foreign key that references `employees.id`.
- Database sessions are closed after use.
- Failed database changes are rolled back.

## What I Learned

I learned how to connect a FastAPI application to a MySQL database using SQLAlchemy. I also learned how to use database models, sessions, CRUD operations, validations, database transactions and test API responses using Swagger UI.

In Task 3, I learned how to implement search, filtering and pagination using SQLAlchemy queries. I also learned how query parameters work in FastAPI and how to validate values such as limit, offset and work mode.

In Task 4, I learned how to create a WorkItem model and connect it with the Employee model using a foreign key and SQLAlchemy relationship. I also learned how to implement work item CRUD operations, filtering, combined filters, pagination, validation and assigned employee details in API responses.

In Task 5, I learned how to implement status transition validation, reuse business logic, preserve existing status during PUT updates, and calculate work item summaries for employees.

## Difficulties

I faced difficulties while setting up the MySQL connection, configuring the database connection details, handling duplicate email validation and understanding SQLAlchemy database operations. I also faced some issues while testing the APIs using Swagger UI.

During Task 3, I faced difficulties while implementing the pagination response structure, combining multiple filters and testing different query parameter combinations.

During Task 4, I faced difficulties while implementing the Employee and WorkItem relationship, handling the assigned employee response, testing combined filters and pagination, and validating invalid status, priority and employee values.

During Task 5, I faced difficulties while implementing status transition rules, handling invalid status inputs and verifying the employee work summary after reassignment and deletion.

## Assumptions

- Employee and work item records are stored in the MySQL database and remain available after application restarts.
- Database credentials are stored locally in the `.env` file and are not committed to the repository.
- Fictional employee and work item data is used for testing.
