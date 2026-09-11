from sqlalchemy import create_engine, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


# SQLite database connection
engine = create_engine(
    "sqlite:///tasks.db",
    connect_args={"check_same_thread": False}
)


# Creates database sessions
SessionLocal = sessionmaker(bind=engine)


# Base class for all SQLAlchemy models
class Base(DeclarativeBase):
    pass


# -------------------------
# User Database Model
# -------------------------
class UserRow(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))


# -------------------------
# Task Database Model
# -------------------------
class TaskRow(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500), default="")
    priority: Mapped[int] = mapped_column(Integer, default=1)
    due_date: Mapped[str] = mapped_column(String(50), default="")
    done: Mapped[bool] = mapped_column(Boolean, default=False)

    # Links each task to the user who created it
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


# -------------------------
# Database Session
# -------------------------
def get_db():
    # Create a database session for the request
    db = SessionLocal()

    try:
        # Provide the session to the endpoint
        yield db
    finally:
        # Always close the session after the request
        db.close()