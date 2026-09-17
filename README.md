FastAPI Employee Management

Project Description

This project is a FastAPI backend for managing employee records.

Employee records are stored in a MySQL database using SQLAlchemy. The records remain available even after the application is restarted.

Technologies Used

* Python 3.12
* FastAPI
* Pydantic
* MySQL
* SQLAlchemy
* PyMySQL
* Uvicorn
* Swagger UI
* Git

Employee Fields

* ID
* Name
* Email
* Department
* Primary Skill
* Location
* Work Mode
* Is Active
* Created At

APIs

* POST /employees
* GET /employees
* GET /employees/{id}
* PUT /employees/{id}
* DELETE /employees/{id}
* GET /health

Validation

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

Database Setup

Create a MySQL database named "employee_db".

The application uses SQLAlchemy and PyMySQL to connect to MySQL and perform create, read, update and delete operations.

The "employees" table is created using the SQLAlchemy model when the application starts.

The email field has a database-level unique constraint.

Database sessions are closed after use.

Database Configuration

Create a local ".env" file in the project root and add the database connection details.

DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=employee_db

A ".env.example" file is also included with placeholder values for reference.

Do not commit the ".env" file or database passwords to GitHub.

How to Run

Create and activate a virtual environment.

Install dependencies:

pip install -r requirements.txt

Start the application:

uvicorn app.main:app --reload

Open Swagger UI:

http://127.0.0.1:8000/docs

What I Learned

I learned how to connect a FastAPI application to a MySQL database using SQLAlchemy. I also learned how to use database models, sessions, CRUD operations, validations, database transactions, and test API responses using Swagger UI.

Difficulties

I faced difficulties while setting up the MySQL connection, configuring the database connection details, handling duplicate email validation, and understanding SQLAlchemy database operations. I also faced some issues while testing the APIs using Swagger UI.

Assumptions

Employee records are stored in the MySQL database and remain available after application restarts.
Database credentials are stored locally in the ".env" file and are not committed to the repository.
Fictional employee data is used for testing.