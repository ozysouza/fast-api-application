# FastAPI Post Application

## Technology Stack and Features

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
    - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database.
    - 🐋 [Docker Compose](https://www.docker.com) for development and production.
    - 🔒 Secure password hashing by default.
    - 🔑 JWT (JSON Web Token) authentication.
    - ✅ Tests with [Pytest](https://pytest.org).
    - 🏭 CI (continuous integration) and CD (continuous deployment) based on GitHub Actions.

# Getting Started
Prerequisites
- Python 3.7+
- Postgres Server
- Virtual Environment (venv)

# Installation
Clone the Repository:
- git clone https://github.com/ozysouza/fast-api-application.git
- cd your-repo-name

# Create and Activate a Virtual Environment:
1. pip3 install virtualenv

2. virtualenv venv

3. source .venv/bin/activate

4. which python - Check source

5. Deactivate virtual environment: deactivate

# Install Dependencies:
- pip install -r requirements.txt

- On the .env file, fill up the variables with your DB settings.

# Running the application:

Navigate to app folder and run the following command:
- fastapi dev main.py

- The endpoints can be tested through the address http://127.0.0.1:8000/docs#/

![fastapi](https://github.com/user-attachments/assets/4201341b-818e-44a2-9e04-3fff932289ac)
