# Simple Task Manager API

This project implements a basic RESTful API for managing tasks. It allows users to create, retrieve, update, and delete tasks.

## Features
- Create a new task with a title, description, and due date.
- Retrieve a list of all tasks.
- Retrieve a specific task by its ID.
- Update an existing task (title, description, due date, status).
- Delete a task.

## Technology Stack
- Python 3.9+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate (for database migrations)
- SQLite (for simplicity, can be swapped for PostgreSQL/MySQL)

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd simple_task_manager
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r src/requirements.txt
    ```

4.  **Set up environment variables:**
    Copy `src/.env.example` to `src/.env` and fill in the necessary values.
    ```bash
    cp src/.env.example src/.env
    ```
    For SQLite, `DATABASE_URL` can be `sqlite:///./tasks.db`.
    `SECRET_KEY` should be a long, random string.

5.  **Initialize and migrate the database:**
    (Ensure you are in the `src` directory or set `FLASK_APP` environment variable appropriately)
    ```bash
    cd src
    export FLASK_APP=app.py  # On Windows: set FLASK_APP=app.py
    flask db init  # Only if migrations folder doesn't exist
    flask db migrate -m "Initial task model"
    flask db upgrade
    cd ..
    ```

6.  **Run the application:**
    ```bash
    cd src
    flask run
    ```
    The API will be available at `http://127.0.0.1:5000`.

## API Endpoints

Refer to the Technical Design Document (`docs/TaskManager_TLD.md`) for detailed API specifications.

## Project Structure
- `docs/`: Contains PRD, TLD, and Compliance documents.
- `src/`: Contains the main application code.
  - `app.py`: Flask app factory and core setup.
  - `models.py`: Database models.
  - `routes.py`: API route definitions.
  - `utils.py`: Helper functions.
  - `config.py`: Application configuration.
  - `requirements.txt`: Dependencies.
  - `.env.example`: Environment variable template.
- `tests/`: Unit and integration tests.

## Intended for Saarthi Code Review

This project has been created with specific areas intended for review by the Saarthi AI Code Review Assistant. It includes examples of:
- Potential compliance oversights.
- Code quality issues (e.g., hardcoding, error handling).
- Readability concerns.
- Minor linting inconsistencies.
- Potential logical errors or missing edge case handling.
- Incomplete features compared to PRD.
