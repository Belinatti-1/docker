import os
from contextlib import asynccontextmanager

import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI
from pydantic import BaseModel


def get_connection():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        dbname=os.environ["DB_NAME"],
        row_factory=dict_row,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
    yield


app = FastAPI(lifespan=lifespan)


class Item(BaseModel):
    name: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/items", status_code=201)
def create_item(item: Item):
    with get_connection() as conn:
        result = conn.execute(
            "INSERT INTO items (name) VALUES (%s) RETURNING id, name",
            (item.name,),
        )
        return result.fetchone()


@app.get("/items")
def list_items():
    with get_connection() as conn:
        result = conn.execute(
            "SELECT id, name FROM items ORDER BY id"
        )
        return result.fetchall()
