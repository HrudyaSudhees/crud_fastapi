# Person CRUD API

A basic REST API built using **FastAPI**, **PostgreSQL**, and **Psycopg** to perform CRUD (Create, Read, Update, Delete) operations on person records.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- Psycopg 3
- Pydantic
- Uvicorn

## Project Structure

```text
person_crud/
├── main.py
├── database.py
├── schema.sql
├── requirements.txt
├── README.md
├── .env
├── .env.example
├── .gitignore
└── venv/
```

- `main.py` — FastAPI application and CRUD endpoints.
- `database.py` — PostgreSQL connection configuration.
- `schema.sql` — SQL statement defining the `persons` table.
- `.env` — Database connection configuration; do not commit this file.
- `.env.example` — Example database configuration.

## Setup and Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd person_crud
```

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

### 4. Configure the database

Create a PostgreSQL database named `person_db` and a database user named `person_user`. Grant the user the required database and table permissions.

Create a `.env` file in the project directory:

```text
DATABASE_URL=postgresql://person_user:YOUR_PASSWORD@localhost:5432/person_db
```

Replace `YOUR_PASSWORD` with your actual PostgreSQL password.

### 5. Create the database table

Run the schema file against the target database:

```bash
psql -h localhost -U person_user -d person_db -f schema.sql
```

Enter the database user's password when prompted.

The `schema.sql` file defines the `persons` table with these columns:

| Column | Type | Description |
|---|---|---|
| `id` | SERIAL PRIMARY KEY | Automatically generated unique ID |
| `name` | VARCHAR(100) | Person's name |
| `gender` | VARCHAR(30) | Gender |
| `age` | INTEGER | Age |
| `dob` | DATE | Date of birth |
| `address` | TEXT | Address |
| `blood_group` | VARCHAR(5) | Blood group |
| `time_zone` | VARCHAR(100) | Time zone |

### 6. Start the API

```bash
uvicorn main:app --reload
```

The API runs locally at:

`http://127.0.0.1:8000`

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check whether the API is running |
| POST | `/persons` | Create a person |
| GET | `/persons` | Retrieve all persons |
| GET | `/persons/{person_id}` | Retrieve a person by ID |
| PUT | `/persons/{person_id}` | Update a person's details |
| DELETE | `/persons/{person_id}` | Delete a person by ID |

## API Documentation

Once the application is running, open the interactive Swagger UI:

`http://127.0.0.1:8000/docs`

Use Swagger UI to test the endpoints and inspect their responses.

## Notes

- The database must be running before you start using the API.
- Run `schema.sql` against the same database specified by `DATABASE_URL`.
- `PUT` expects the complete person payload.
- Keep `.env` and other files containing secrets out of version control.