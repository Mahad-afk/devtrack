import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import Project, Task
from .routers import projects, tasks

Base.metadata.create_all(bind=engine)
app = FastAPI(title="DevTrack API", description="Developer productivity and project tracking API.", version="0.1.0")
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(CORSMiddleware, allow_origins=[origin.strip() for origin in origins], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(projects.router)
app.include_router(tasks.router)

@app.get("/api/health", tags=["system"])
def health():
    return {"status": "ok", "service": "devtrack-api"}

@app.get("/api/dashboard", tags=["dashboard"])
def dashboard(db: Session = Depends(get_db)):
    project_count = db.query(Project).count()
    task_count = db.query(Task).count()
    completed_count = db.query(Task).filter(Task.completed.is_(True)).count()
    return {"project_count": project_count, "task_count": task_count, "open_count": task_count - completed_count, "completed_count": completed_count, "completion_rate": round(completed_count / task_count * 100, 1) if task_count else 0.0}
