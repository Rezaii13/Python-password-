from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()


class User(Base):
    """
    User model for the authentication system.
    
    Attributes:
        id (int): Primary key for the user
        username (str): Unique username for login
        email (str): Unique email address
        password_hash (str): Hashed password for security
        first_name (str): User's first name
        last_name (str): User's last name
        is_active (bool): Flag to indicate if user account is active
        created_at (datetime): Timestamp of user creation
        updated_at (datetime): Timestamp of last update
    """
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(120), nullable=True)
    last_name = Column(String(120), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def set_password(self, password):
        """
        Hash and set the user's password.
        
        Args:
            password (str): The plain text password to hash
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verify if the provided password matches the stored hash.
        
        Args:
            password (str): The plain text password to verify
            
        Returns:
            bool: True if password is correct, False otherwise
        """
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """
        Get the user's full name.
        
        Returns:
            str: The user's full name or username if names not provided
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.username
    
    def __repr__(self):
        """Return a string representation of the User object."""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    def to_dict(self):
        """
        Convert user object to dictionary (useful for API responses).
        
        Returns:
            dict: Dictionary representation of the user
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
