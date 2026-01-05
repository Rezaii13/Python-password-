"""
SQLAlchemy Database Configuration and Session Management
This module provides database initialization, configuration, and session management
for the application using SQLAlchemy ORM.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL configuration
# Supports both SQLite (default) and other databases via DATABASE_URL env variable
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./password_manager.db"
)

# Create database engine
# For SQLite, we need to add check_same_thread=False for thread safety in development
engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    **engine_kwargs,
    echo=os.getenv("SQL_ECHO", "False").lower() == "true"  # Set to True for SQL logging
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Declarative base for model definitions
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI or other frameworks to get database session.
    Usage in FastAPI:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database by creating all tables based on defined models.
    Should be called once at application startup.
    """
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """
    Drop all tables from the database.
    WARNING: This is destructive and will remove all data!
    Use only in development/testing environments.
    """
    Base.metadata.drop_all(bind=engine)


def get_session() -> Session:
    """
    Get a direct database session.
    Note: Remember to close the session when done.
    
    Returns:
        Session: SQLAlchemy database session
    """
    return SessionLocal()


# Example usage and testing
if __name__ == "__main__":
    # Initialize the database
    init_db()
    print(f"Database initialized successfully!")
    print(f"Database URL: {DATABASE_URL}")
