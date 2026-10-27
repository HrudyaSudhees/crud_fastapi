import os
from pathlib import Path

import requests
import psycopg
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

BASE_URL = "http://127.0.0.1:8000"
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured.")


def get_person_from_db(person_id):
    """Read a person directly from PostgreSQL."""
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, gender, age, dob, address,
                       blood_group, time_zone
                FROM persons
                WHERE id = %s
                """,
                (person_id,),
            )
            row = cur.fetchone()

            if row is None:
                return None

            columns = [column.name for column in cur.description]
            return dict(zip(columns, row))


def test_crud():
    person = {
        "name": "Test Person",
        "gender": "Female",
        "age": 25,
        "dob": "2001-05-10",
        "address": "Bengaluru, India",
        "blood_group": "O+",
        "time_zone": "Asia/Kolkata",
    }

    person_id = None

    try:
        # 1. POST: Create a person through the API.
        response = requests.post(
            f"{BASE_URL}/persons",
            json=person,
            timeout=10,
        )
        #print("Status code:", response.status_code)
        assert response.status_code == 201, response.text

        created = response.json()
        person_id = created["id"]

        # Verify the record exists in PostgreSQL.
        db_person = get_person_from_db(person_id)
        assert db_person is not None, "POST failed: row missing from database."

        for key, value in person.items():
            assert str(db_person[key]) == str(value), (
                f"POST mismatch for {key}: {db_person[key]!r} != {value!r}"
            )

        print("PASS: POST response and database record verified.")

        # 2. GET all: Verify the new person is returned.
        response = requests.get(f"{BASE_URL}/persons", timeout=10)
        assert response.status_code == 200, response.text

        people = response.json()
        assert any(p["id"] == person_id for p in people)
        print("PASS: GET all returns the created person.")

        # 3. GET one: Verify response against the database.
        response = requests.get(
            f"{BASE_URL}/persons/{person_id}",
            timeout=10,
        )
        assert response.status_code == 200, response.text

        api_person = response.json()
        db_person = get_person_from_db(person_id)

        assert db_person is not None
        for key in person:
            assert str(api_person[key]) == str(db_person[key])

        print("PASS: GET by ID matches the database.")

        # 4. PUT: Update the person through the API.
        updated = person.copy()
        updated["name"] = "Updated Test Person"
        updated["age"] = 26

        response = requests.put(
            f"{BASE_URL}/persons/{person_id}",
            json=updated,
            timeout=10,
        )
        assert response.status_code == 200, response.text

        # Verify PostgreSQL contains the updated values.
        db_person = get_person_from_db(person_id)
        assert db_person is not None
        assert db_person["name"] == updated["name"]
        assert db_person["age"] == updated["age"]

        print("PASS: PUT changes verified in the database.")

        # 5. DELETE: Delete through the API.
        response = requests.delete(
            f"{BASE_URL}/persons/{person_id}",
            timeout=10,
        )
        assert response.status_code in (200, 204), response.text

        # Verify the row is gone from PostgreSQL.
        db_person = get_person_from_db(person_id)
        assert db_person is None, "DELETE failed: row still exists."

        print("PASS: DELETE verified in the database.")

        # 6. Confirm the API also reports the person as missing.
        response = requests.get(
            f"{BASE_URL}/persons/{person_id}",
            timeout=10,
        )
        assert response.status_code == 404, response.text

        print("PASS: Deleted person returns HTTP 404.")
        print("\nAll CRUD and database verification tests passed!")

    finally:
        # Safety cleanup if a test fails before the API DELETE.
        # Only deletes the specific record created by this test.
        if person_id is not None:
            try:
                with psycopg.connect(DATABASE_URL) as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            "DELETE FROM persons WHERE id = %s",
                            (person_id,),
                        )
            except psycopg.Error as exc:
                print(f"Cleanup warning: {exc}")


if __name__ == "__main__":
    test_crud()