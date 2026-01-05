"""
SQLAlchemy ORM Models for User Authentication System
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create base class for all models
Base = declarative_base()


class User(Base):
    """
    User Model for Authentication System
    
    Attributes:
        id: Primary key - unique identifier for each user
        username: Unique username for login
        email: Unique email address
        hashed_password: Securely hashed password (never store plain text)
        is_active: Boolean flag to indicate if user account is active
        created_at: Timestamp when user account was created
        updated_at: Timestamp when user account was last updated
    """
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        """String representation of User object"""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', is_active={self.is_active})>"
    
    def to_dict(self):
        """Convert User object to dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# Database configuration and session management
def get_db_engine(database_url: str):
    """
    Create and return SQLAlchemy engine
    
    Args:
        database_url: Database connection URL (e.g., 'sqlite:///./test.db')
    
    Returns:
        SQLAlchemy Engine object
    """
    return create_engine(database_url, connect_args={"check_same_thread": False} if "sqlite" in database_url else {})


def get_db_session(engine):
    """
    Create and return database session factory
    
    Args:
        engine: SQLAlchemy Engine object
    
    Returns:
        SessionLocal: Session factory for database operations
    """
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db(engine):
    """
    Initialize database by creating all tables
    
    Args:
        engine: SQLAlchemy Engine object
    """
    Base.metadata.create_all(bind=engine)


# Example usage for testing
if __name__ == "__main__":
    # This is just an example of how to use the models
    # In production, you should use a proper configuration file
    
    DATABASE_URL = "sqlite:///./auth.db"
    
    # Create engine and session
    engine = get_db_engine(DATABASE_URL)
    SessionLocal = get_db_session(engine)
    
    # Initialize database
    init_db(engine)
    
    print("Database initialized successfully!")
    print("User model is ready for use.")
