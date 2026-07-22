from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine

from app.api import students


@asynccontextmanager
async def on_startup(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Database tables created")

    yield

    print("Shutting down Smart Attendance System")


app = FastAPI(
    title="Smart Attendance System",
    version="1.0.0",
    lifespan=on_startup,
)

# CORS — allow React/Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "version": app.version,
    }

app.include_router(students.router)