from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import date

from database import get_connection

app = FastAPI(title="Basic person CRUD API")

class Person(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    gender: str
    age: int = Field(ge=0, le=150)
    dob: date
    address: str
    blood_group: str
    time_zone: str

@app.get("/")
def home():
    return {"message": "Person CRUD API is running..."}
#create a person
@app.post("/persons", status_code=201)
def create_person(person:Person):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO persons
                (name, gender, age, dob, address, blood_group, time_zone)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                (
                    person.name,
                    person.gender,
                    person.age,
                    person.dob,
                    person.address,
                    person.blood_group,
                    person.time_zone,
                ),
            )
            row = cur.fetchone()

            if row is None:
                raise HTTPException(
                    status_code=404,
                    detail="Person not found",
                )

            columns = [column.name for column in cur.description]
            return dict(zip(columns, row))
#read all people
@app.get("/persons")
def get_all_people():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM persons ORDER BY id")
            rows = cur.fetchall()

            columns = [column.name for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]
#read one person with person id
@app.get("/persons/{person_id}")
def get_one_person(person_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM persons WHERE id = %s",
                (person_id,),
            )
            row = cur.fetchone()

            if row is None:
                raise HTTPException(
                    status_code=404,
                    detail="Person not found",
                )
            columns = [column.name for column in cur.description]
            return dict(zip(columns, row))
#update person 
@app.put("/persons/{person_id}")
def update_person(person_id: int, person: Person):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE persons
                SET name = %s, 
                    gender = %s, 
                    age = %s, 
                    dob = %s, 
                    address = %s, 
                    blood_group = %s, 
                    time_zone = %s
                WHERE id = %s
                RETURNING *
                """,
                (
                    person.name,
                    person.gender,
                    person.age,
                    person.dob,
                    person.address,
                    person.blood_group,
                    person.time_zone,
                    person_id,
                ),
            )
            row = cur.fetchone()

            if row is None:
                raise HTTPException(
                    status_code=404,
                    detail="Person not found",
                )

            columns = [column.name for column in cur.description]
            return dict(zip(columns, row))
#delete perosn with person id
@app.delete("/persons/{person_id}", status_code=204)
def delete_person(person_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM persons WHERE id = %s RETURNING id",
                (person_id,),
            )

            row = cur.fetchone()
            if row is None:
                raise HTTPException(
                    status_code=404,
                    detail="Person not found",
                )
    return None