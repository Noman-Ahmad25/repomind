import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import Generator

# Default to the connection string defined in our architecture
DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql+psycopg://postgres:password@localhost:5432/repomind"
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modern SQLAlchemy 2.0 style declarative base that Mypy understands
class Base(DeclarativeBase):
    pass

def get_db() -> Generator[Session, None, None]:
    """Dependency to get the database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()