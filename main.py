from fastapi import FastAPI

from database import engine, Base
from routers import tasks, users, auth


Base.metadata.create_all(engine)

app = FastAPI(title="Task API")


# -------------------------
# Include Task Router
# -------------------------

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth.router)

# -------------------------
# Root Endpoint
# -------------------------

@app.get("/")
def home():
    return {"message": "FastAPI is working!"}


# -------------------------
# Health Check
# -------------------------
@app.get("/health")
def check_health():
    return {
        "status": "ok",
        "message": "Task API is healthy"
    }