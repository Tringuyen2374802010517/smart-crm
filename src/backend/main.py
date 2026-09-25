import sqlite3

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
def home():
    return "Hello Smart CRM"


@app.get("/db-check")
def db_check():
    conn = sqlite3.connect("smartcrm.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    conn.close()

    return {
        "status": "OK",
        "database": "SQLite",
        "result": result[0]
    }