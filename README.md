# FastAPI Employee Management

## Project Description

This project is a FastAPI backend application for managing employee records and work items. Employee and work item data are stored in a MySQL database using SQLAlchemy. The data remains available after the application is restarted.

The project includes employee management, search, filtering, pagination, work item management, controlled work item status transitions, and employee work summary functionality.

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
- `GET /employees/{employee_id}`
- `PUT /employees/{employee_id}`
- `DELETE /employees/{employee_id}`
- `GET /health`

## Employee Validation

- Required employee fields are validated.
- Empty or whitespace-only required fields are rejected.
- Email format is validated.
- Duplicate email addresses are not allowed.
- Email uniqueness is checked without treating uppercase and lowercase letters as different.
- Work mode accepts `WFH` or `WFO`.
- Employee ID must be greater than zero.
- A 404 Not Found response is returned when an employee does not exist.
- Employee IDs are generated automatically by the database.
- `is_active` is set to `true` by default.
- `created_at` is generated when an employee is created and preserved during updates.
- Failed database changes are rolled back so that subsequent requests can continue working.

# Task 3 - Search, Filtering and Pagination

Task 3 adds search, filtering, and pagination to the `GET /employees` endpoint.

## Query Parameters

- `search` - Searches employee names using partial and case-insensitive matching.
- `department` - Filters employees by department.
- `work_mode` - Filters employees by `WFH` or `WFO`.
- `is_active` - Filters employees by active or inactive status.
- `limit` - Maximum number of records to return. Default is 10. Allowed values are 1 to 100.
- `offset` - Number of records to skip. Default is 0. Negative values are not allowed.

## Example Request

`GET /employees?department=Engineering&work_mode=WFH&limit=5&offset=0`

## Employee List Response

The `GET /employees` endpoint returns a paginated response.

Example:

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

## Task 3 Testing

The following scenarios were tested using Swagger UI:

- Employee name search.
- Department filtering.
- Work mode filtering.
- Active and inactive filtering.
- Combined filters.
- Partial name search.
- Pagination using limit and offset.
- No matching results.
- Offset greater than the number of matching records.
- Invalid limit values.
- Negative offset validation.
- Invalid work mode validation.

Search, filtering, and pagination are performed using SQLAlchemy queries.

# Task 4 - Work Item Management

Task 4 adds work item management to the Employee Management API. Each work item is assigned to an existing employee through a foreign key relationship.

## Work Item Fields

- ID
- Title
- Description
- Employee ID
- Status
- Priority
- Due Date
- Created At
- Assigned Employee

## Work Item Status

- `TODO`
- `IN_PROGRESS`
- `COMPLETED`

## Work Item Priority

- `LOW`
- `MEDIUM`
- `HIGH`

## Work Item APIs

- `POST /work-items`
- `GET /work-items`
- `GET /work-items/{work_item_id}`
- `PUT /work-items/{work_item_id}`
- `DELETE /work-items/{work_item_id}`

## Work Item Query Parameters

The `GET /work-items` endpoint supports search, filtering, and pagination.

- `search` - Searches work item titles using partial and case-insensitive matching.
- `employee_id` - Filters work items by assigned employee.
- `status` - Filters work items by status.
- `priority` - Filters work items by priority.
- `limit` - Maximum number of records to return. Default is 10. Allowed values are 1 to 100.
- `offset` - Number of records to skip. Default is 0. Negative values are not allowed.

## Example Request

`GET /work-items?employee_id=2&status=TODO&priority=MEDIUM&limit=10&offset=0`

## Work Item Response

Each work item response includes the assigned employee details.

Example:

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
    "email": "babitha1@example.com"
  }
}


## Work Item List Response

The `GET /work-items` endpoint returns a paginated response.

Example:

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

## Work Item Validation

- Title is required.
- Empty or whitespace-only titles are rejected.
- Employee ID must be greater than zero.
- The assigned employee must exist.
- Status accepts `TODO`, `IN_PROGRESS`, or `COMPLETED`.
- Priority accepts `LOW`, `MEDIUM`, or `HIGH`.
- Work item ID must be greater than zero.
- A 404 Not Found response is returned when a work item or employee does not exist.
- Database changes are rolled back when a database error occurs.

## Employee and Work Item Relationship

A work item belongs to an employee through the `employee_id` foreign key.

The SQLAlchemy relationship connects the `Employee` and `WorkItem` models. Each work item response also includes the assigned employee's:

- ID
- Name
- Email

## Task 4 Testing

The following scenarios were tested using Swagger UI:

- Create a work item.
- Create a work item with a non-existing employee.
- Get a work item by ID.
- Search work items by title.
- Filter by employee ID.
- Filter by status.
- Filter by priority.
- Combined filters.
- Pagination using limit and offset.
- Update a work item.
- Reassign a work item to another employee.
- Invalid status validation.
- Invalid priority validation.
- Blank title validation.
- Delete a work item.
- Verify that a deleted work item returns 404.
- Verify that data remains available after application restart.
- Verify that existing employee APIs continue working.

Search, filtering, pagination, and ordering are performed using SQLAlchemy queries.

# Task 5 - Work Item Status Management and Work Summary

Task 5 adds controlled work item status transitions and employee work summary functionality.

## Work Item Status Transition Rules

The application supports these statuses:

- `TODO`
- `IN_PROGRESS`
- `COMPLETED`

The allowed status transitions are:

- `TODO` to `IN_PROGRESS`
- `IN_PROGRESS` to `COMPLETED`

Additional rules:

- New work items must start with `TODO` status.
- Direct creation with `IN_PROGRESS` or `COMPLETED` is rejected.
- Invalid status transitions return a 400 Bad Request response.
- Updating a work item with its current status is allowed.
- A PUT request that omits status preserves the existing status.
- Invalid status values in the PATCH request are rejected with a 422 validation response.
- Missing or null status in the PATCH request is rejected with a 422 validation response.
- A 404 Not Found response is returned when the requested work item does not exist.
- An invalid status transition is rejected without updating other work item fields.

## Work Item Status API

`PATCH /work-items/{work_item_id}/status`

This endpoint updates a work item's status after validating the requested transition.

Example request:

{
  "status": "COMPLETED"
}

The endpoint uses shared status transition logic from the service layer. The PUT and PATCH endpoints use the same transition validation rules.

## Employee Work Summary API

`GET /employees/{employee_id}/work-summary`

This endpoint returns a summary of the work items currently assigned to an employee.

### Work Summary Fields

- `employee_id` - Employee ID.
- `total_work_items` - Total number of currently assigned work items.
- `todo` - Number of work items with `TODO` status.
- `in_progress` - Number of work items with `IN_PROGRESS` status.
- `completed` - Number of work items with `COMPLETED` status.

### Example Response

{
  "employee_id": 6,
  "total_work_items": 1,
  "todo": 0,
  "in_progress": 0,
  "completed": 1
}

The counts reflect work items currently assigned to the employee. The total count equals the sum of the three status counts. If an employee has no assigned work items, the counts are zero. A 404 Not Found response is returned when the employee does not exist.

## Task 5 Testing

The following scenarios were tested using Swagger UI:

- Valid status transition.
- Invalid status transition.
- Updating a work item with its current status.
- Missing status in a PATCH request.
- Null status in a PATCH request.
- Invalid status value in a PATCH request.
- Creating a work item with a non-TODO status.
- Updating a work item without providing status and preserving the existing status.
- Rejecting an invalid PUT status transition without changing other fields.
- Work summary counts for an employee.
- Work summary request for a non-existing employee.
- Status update request for a non-existing work item.

# Database Setup

Create a MySQL database named `employee_db`.
The application uses SQLAlchemy and PyMySQL to connect to MySQL and perform database operations.
The `employees` and `work_items` tables are created using SQLAlchemy models when the application starts.
- The employee email field has a database-level unique constraint.
- The `work_items.employee_id` field is a foreign key referencing `employees.id`.
- Database sessions are closed after use.
- Database changes are committed when successful.
- Database changes are rolled back when database errors occur.

# Database Configuration

Create a local `.env` file in the project root and add the database connection details.

DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=employee_db


A `.env.example` file with placeholder values can be included for reference.

**Important:** Do not commit the `.env` file or database passwords to GitHub.

# How to Run

## 1. Create and Activate a Virtual Environment

Create a virtual environment and activate it using the appropriate command for your operating system.

## 2. Install Dependencies

pip install -r requirements.txt

## 3. Start the Application

uvicorn app.main:app --reload

## 4. Open Swagger UI

Open the following URL in your browser:

`http://127.0.0.1:8000/docs`

Use Swagger UI to execute and test the API endpoints.

# What I Learned

## Task 1 and Task 2

- How to build REST APIs using FastAPI.
- How to define request and response schemas using Pydantic.
- How to implement CRUD operations.
- How to connect FastAPI to MySQL using SQLAlchemy.
- How to use database models and sessions.
- How to validate inputs and handle HTTP errors.
- How to manage database transactions and rollbacks.

## Task 3

- How to implement search, filtering, and pagination using SQLAlchemy queries.
- How to use query parameters in FastAPI.
- How to validate limit, offset, and work mode values.
- How to combine multiple filters.

## Task 4

- How to create a WorkItem model.
- How to connect Employee and WorkItem using a foreign key and SQLAlchemy relationship.
- How to implement work item CRUD operations.
- How to include assigned employee details in responses.
- How to validate work item fields and employee assignments.

## Task 5

- How to implement controlled status transitions.
- How to validate PATCH requests.
- How to preserve existing values when fields are omitted from PUT requests.
- How to reuse status transition logic between endpoints.
- How to calculate employee work summaries using SQLAlchemy queries.
- How to test successful requests, validation errors, and missing-resource responses using Swagger UI.

# Difficulties

During development, I faced difficulties while:

- Setting up the MySQL connection and configuring database credentials.
- Handling duplicate email validation.
- Understanding SQLAlchemy database operations.
- Implementing pagination response structures.
- Combining multiple search and filter parameters.
- Establishing the Employee and WorkItem relationship.
- Returning assigned employee details.
- Validating status and priority values.
- Implementing valid and invalid status transitions.
- Preserving existing status during PUT updates.
- Testing API responses and debugging errors using Swagger UI.

These challenges helped me understand API development, database integration, validation, and debugging.

# Assumptions

- Employee and work item records are stored in MySQL.
- Records remain available after the application restarts.
- Database credentials are stored locally in the `.env` file.
- The `.env` file and database passwords are not committed to the repository.
- Fictional employee and work item data is used for testing.
