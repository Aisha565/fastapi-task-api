from pydantic import BaseModel, ConfigDict, Field


# -------------------------
# Task Creation Schema
# -------------------------

class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = ""
    priority: int = Field(default=1, ge=1, le=5)
    due_date: str = ""


# -------------------------
# Task Update Schema
# -------------------------

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = None
    priority: int | None = Field(default=None, ge=1, le=5)
    due_date: str | None = None


# -------------------------
# Task Response Schema
# -------------------------

class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str = ""
    priority: int = 1
    due_date: str = ""
    done: bool = False


# -------------------------
# User Registration Schema
# -------------------------

class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=8)