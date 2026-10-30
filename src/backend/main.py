from src.backend.api.auth_api import router as auth_router
from src.backend.api.appointment_api import router as appointment_router
from src.backend.api.technician_api import router as technician_router

import sqlite3

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, JSONResponse

from src.backend.api.ticket_api import router as ticket_router
from src.backend.api.assignment_api import router as assignment_router

from src.backend.services.exceptions import BusinessError, NotFoundError

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.exception_handler(NotFoundError)
async def handle_not_found(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": exc.message})


@app.exception_handler(BusinessError)
async def handle_business_error(request: Request, exc: BusinessError):
    return JSONResponse(status_code=400, content={"detail": exc.message})


# Allow the Vite frontend to call FastAPI during development.
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
app.include_router(technician_router)

app.include_router(appointment_router)

app.include_router(auth_router)
