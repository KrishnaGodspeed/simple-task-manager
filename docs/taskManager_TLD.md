# Technical Design Document: Simple Task Manager API

**Version:** 1.0
**Date:** 2023-10-27
**Author:** Engineering Team

## 1. Introduction
This document outlines the technical design for the Simple Task Manager API, based on the requirements specified in `TaskManager_PRD.md`.

## 2. Architecture Overview
The system will be a monolithic RESTful API built using Python and the Flask framework. It will interact with an SQLite database (for development/testing) via Flask-SQLAlchemy ORM.

- **Presentation Layer:** Flask routes handling HTTP requests and responses.
- **Business Logic Layer:** Service functions within route handlers or separate utility modules.
- **Data Access Layer:** SQLAlchemy models and session management.

## 3. Technology Stack
- **Programming Language:** Python 3.9+
- **Framework:** Flask
- **ORM:** Flask-SQLAlchemy
- **Database:** SQLite (default), configurable for PostgreSQL/MySQL
- **Migrations:** Flask-Migrate
- **Environment Management:** `python-dotenv`

## 4. Data Model
Database: `tasks.db` (SQLite)

**Table: `tasks`**

| Column        | Data Type     | Constraints                        | Description                       |
|---------------|---------------|------------------------------------|-----------------------------------|
| `id`          | Integer       | Primary Key, Auto Increment        | Unique identifier for the task    |
| `title`       | String(120)   | Not Null                           | Title of the task                 |
| `description` | Text          | Nullable                           | Detailed description of the task  |
| `due_date`    | DateTime      | Nullable                           | When the task is due              |
| `status`      | String(20)    | Not Null, Default: 'pending'       | Current status of the task        |
| `created_at`  | DateTime      | Not Null, Default: current_timestamp | Timestamp of creation             |
| `updated_at`  | DateTime      | Not Null, Default: current_timestamp, On Update: current_timestamp | Timestamp of last update        |

**Allowed Statuses:** "pending", "in progress", "completed"

## 5. API Endpoint Design

**Base URL:** `/api/v1`

**5.1. Create Task**
- **Endpoint:** `POST /tasks`
- **Request Body (JSON):**
  ```json
  {
    "title": "string (required)",
    "description": "string (optional)",
    "due_date": "YYYY-MM-DDTHH:MM:SS (optional, ISO 8601)"
     Success Response (201 Created):

          
    {
      "id": 1,
      "title": "string",
      "description": "string",
      "due_date": "YYYY-MM-DDTHH:MM:SS",
      "status": "pending",
      "created_at": "YYYY-MM-DDTHH:MM:SS",
      "updated_at": "YYYY-MM-DDTHH:MM:SS"
    }

        

    IGNORE_WHEN_COPYING_START

    Use code with caution. Json
    IGNORE_WHEN_COPYING_END

    Error Responses:

        400 Bad Request: Invalid input (e.g., missing title, invalid date format).

        500 Internal Server Error: Server-side issues.

5.2. Get All Tasks

    Endpoint: GET /tasks

    Query Parameters:

        status (optional, string): Filter by status (e.g., pending, in progress, completed)

    Success Response (200 OK):

          
    [
      {
        "id": 1,
        "title": "string",
        "status": "pending"
      },
      {
        "id": 2,
        "title": "string",
        "status": "completed"
      }
    ]

        

    IGNORE_WHEN_COPYING_START

    Use code with caution. Json
    IGNORE_WHEN_COPYING_END

    (Note: PRD FR-002 specifies ID, title, status. Implementation should match this)

5.3. Get Single Task

    Endpoint: GET /tasks/<int:task_id>

    Success Response (200 OK):

          
    {
      "id": 1,
      "title": "string",
      "description": "string",
      "due_date": "YYYY-MM-DDTHH:MM:SS",
      "status": "pending",
      "created_at": "YYYY-MM-DDTHH:MM:SS",
      "updated_at": "YYYY-MM-DDTHH:MM:SS"
    }

        

    IGNORE_WHEN_COPYING_START

    Use code with caution. Json
    IGNORE_WHEN_COPYING_END

    Error Responses:

        404 Not Found: Task with the given ID does not exist.

5.4. Update Task

    Endpoint: PUT /tasks/<int:task_id>

    Request Body (JSON): (All fields optional, at least one must be present)

          
    {
      "title": "string",
      "description": "string",
      "due_date": "YYYY-MM-DDTHH:MM:SS",
      "status": "string (pending, in progress, completed)"
    }

        

    IGNORE_WHEN_COPYING_START

Use code with caution. Json
IGNORE_WHEN_COPYING_END

Success Response (200 OK):

      
{
  "id": 1,
  "title": "string",
  "description": "string",
  "due_date": "YYYY-MM-DDTHH:MM:SS",
  "status": "in progress",
  "created_at": "YYYY-MM-DDTHH:MM:SS",
  "updated_at": "YYYY-MM-DDTHH:MM:SS"
}

    

IGNORE_WHEN_COPYING_START

    Use code with caution. Json
    IGNORE_WHEN_COPYING_END

    Error Responses:

        400 Bad Request: Invalid input.

        404 Not Found: Task not found.

5.5. Delete Task

    Endpoint: DELETE /tasks/<int:task_id>

    Success Response (204 No Content): Empty body.

    Error Responses:

        404 Not Found: Task not found.

6. Security Considerations

    Input Sanitization: All user-provided input must be sanitized to prevent XSS and other injection attacks (SQLAlchemy helps with SQLi).

    Secret Management: SECRET_KEY and DATABASE_URL will be managed via environment variables.

    No Sensitive Data in Logs: Avoid logging raw request bodies if they might contain sensitive information as per PRD FR-009 and OrgPolicy.

    HTTPS: Recommended for production deployment (handled by reverse proxy like Nginx).

7. Error Handling Strategy

    Use standard HTTP status codes.

    Provide JSON error responses: {"error": "message"}.

    Log detailed errors on the server-side for debugging.

8. Database Migrations

Flask-Migrate (Alembic) will be used for schema migrations.

    flask db init

    flask db migrate -m "description"

    flask db upgrade

9. Logging

    Use Flask's built-in logger.

    Log levels: DEBUG, INFO, WARNING, ERROR.

    Production logs should primarily be INFO and above. Avoid DEBUG in production.

10. Future Scalability

    Consider switching from SQLite to PostgreSQL or MySQL for production.

    Stateless API design allows for horizontal scaling with a load balancer.

    Caching strategies (e.g., Redis) can be introduced for frequently accessed data. }
