# Person CRUD API

A REST API built with **FastAPI, PostgreSQL, and Psycopg 3** to perform Create, Read, Update, and Delete (CRUD) operations on person records.

The project includes a Python database initialization script and an API test script that verifies both HTTP responses and the corresponding database state.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- Psycopg 3
- Pydantic
- Uvicorn
- Requests

## Project Structure

```text
person_crud/
├── main.py
├── database.py
├── init_db.py
├── schema.sql
├── test_api.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
└── .env                 # Local only; not committed
```

- `main.py` — FastAPI application and CRUD endpoints.
- `database.py` — PostgreSQL connection configuration.
- `init_db.py` — Initializes the database and executes the SQL schema.
- `schema.sql` — Defines the `persons` table.
- `test_api.py` — Tests API endpoints and verifies database changes.
- `requirements.txt` — Python dependencies.
- `.env.example` — Template for environment configuration.
- `.gitignore` — Excludes secrets and generated files from Git.

## Prerequisites

Install the following before starting:

- Python 3.10 or newer, compatible with the project dependencies.
- PostgreSQL.
- Git.

PostgreSQL must be running before database initialization.

## Setup and Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd person_crud
```

Replace the placeholder with the actual repository URL.

### 2. Create and activate a virtual environment

On Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database connection

Create a PostgreSQL login role if you do not already have one.

For a local development setup, open the PostgreSQL administrator prompt:

```bash
sudo -u postgres psql
```

Create the application user, replacing the password with your own:

```sql
CREATE USER person_user WITH PASSWORD 'YOUR_PASSWORD';
ALTER USER person_user CREATEDB;
\q
```

The `CREATEDB` privilege allows the initialization script to create the target database. It is convenient for local development, but a production application user should generally not have this privilege.

If the role already exists, do not create it again. Ensure its credentials and privileges are configured appropriately.

Create your local `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` so it contains your actual connection string:

```text
DATABASE_URL=postgresql://person_user:YOUR_PASSWORD@localhost:5432/person_db
```

Replace `YOUR_PASSWORD` with the password configured for your PostgreSQL user.

**Never commit `.env` or share your database credentials.**

### 5. Initialize the database

Run:

```bash
python init_db.py
```

The script checks whether `person_db` exists, creates it if necessary, and executes `schema.sql` to initialize the table structure.

The configured database user needs permission to create databases when the target database does not already exist.

If your database already exists but the application user lacks the necessary permissions, ask a PostgreSQL administrator to configure the database and grants.

You do not need to execute `schema.sql` manually.

### 6. Start the API

```bash
uvicorn main:app --reload
```

The API runs at:

http://127.0.0.1:8000

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check whether the API is running |
| POST | `/persons` | Create a person |
| GET | `/persons` | Retrieve all persons |
| GET | `/persons/{person_id}` | Retrieve a person by ID |
| PUT | `/persons/{person_id}` | Update a person's details |
| DELETE | `/persons/{person_id}` | Delete a person by ID |

The API uses appropriate HTTP status codes, including `201 Created` for successful creation and `404 Not Found` when a requested person does not exist.

## API Documentation

With the server running, open Swagger UI:

http://127.0.0.1:8000/docs

Use the interactive documentation to send requests and inspect responses.

## Database Schema

The `persons` table contains:

| Column | Type | Description |
|---|---|---|
| `id` | `SERIAL PRIMARY KEY` | Unique, automatically generated ID |
| `name` | `VARCHAR(100)` | Person's name |
| `gender` | `VARCHAR(30)` | Gender |
| `age` | `INTEGER` | Age |
| `dob` | `DATE` | Date of birth |
| `address` | `TEXT` | Address |
| `blood_group` | `VARCHAR(5)` | Blood group |
| `time_zone` | `VARCHAR(100)` | Time zone |

The SQL definition is maintained in `schema.sql`.

## Testing the API

The `test_api.py` script performs an end-to-end CRUD test and checks the corresponding PostgreSQL state.

It verifies:

1. A person can be created through POST and the row exists in the database.
2. GET all returns the created person.
3. GET by ID returns data consistent with PostgreSQL.
4. PUT updates the record in the database.
5. DELETE removes the record from the database.
6. GET by ID returns `404` after deletion.

### Run the tests

Start the API in one terminal:

```bash
source venv/bin/activate
uvicorn main:app --reload
```

In a second terminal, from the project directory:

```bash
source venv/bin/activate
python test_api.py
```

The test script creates and deletes a real database record. Run it against a development database, not production data.

## Important Notes

- PostgreSQL must be running before the application starts.
- Configure `DATABASE_URL` in `.env`.
- Run `python init_db.py` before starting the API on a fresh database.
- The PUT endpoint expects the complete person payload.
- The API uses Psycopg directly; SQLAlchemy is not required.
- Keep passwords, `.env`, virtual environments, and generated files out of version control.
- The database initialization script creates the schema but does not replace proper database access controls or schema migrations.
