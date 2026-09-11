from pydantic import BaseModel, ConfigDict


# Schema for creating a new task
class TaskCreate(BaseModel):
    title: str
    description: str = ""
    priority: int = 1
    due_date: str = ""


# Schema for partially updating an existing task
# All fields are optional because PATCH updates only the fields provided
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: int | None = None
    due_date: str | None = None


# Schema for returning task data
class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str = ""
    priority: int = 1
    due_date: str = ""
    done: bool = False


# Schema for registering a new user
class UserCreate(BaseModel):
    email: str
    password: str