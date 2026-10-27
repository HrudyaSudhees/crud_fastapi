import os
from pathlib import Path

import psycopg
from psycopg import sql
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

SCHEMA_FILE = Path(__file__).with_name("schema.sql")


def initialize_database():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured.")

    # Parse the connection settings from DATABASE_URL.
    conn_info = psycopg.conninfo.conninfo_to_dict(database_url)

    database_name = conn_info.get("dbname")
    if not database_name:
        raise RuntimeError("Database name is missing from DATABASE_URL.")

    # Connect to the default PostgreSQL database to create our database.
    admin_info = conn_info.copy()
    admin_info["dbname"] = "postgres"

    with psycopg.connect(
        psycopg.conninfo.make_conninfo(**admin_info),
        autocommit=True,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (database_name,),
            )
            database_exists = cur.fetchone() is not None

            if not database_exists:
                cur.execute(
                    sql.SQL("CREATE DATABASE {}").format(
                        sql.Identifier(database_name)
                    )
                )
                print(f"Database '{database_name}' created.")
            else:
                print(f"Database '{database_name}' already exists.")

    # Connect to the target database and create its tables.
    if not SCHEMA_FILE.is_file():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_FILE}")

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(SCHEMA_FILE.read_text(encoding="utf-8"))

    print("Database schema initialized successfully.")


if __name__ == "__main__":
    initialize_database()