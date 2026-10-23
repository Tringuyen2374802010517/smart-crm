
import sqlite3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from src.backend.api.ticket_api import router as ticket_router
from src.backend.api.assignment_api import router as assignment_router

app = FastAPI()

# Allow the Vite frontend to call FastAPI during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


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


app.include_router(ticket_router)
app.include_router(assignment_router)
