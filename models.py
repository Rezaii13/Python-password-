from sqlalchemy import Column, Integer, String, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()


class User(Base):
    """User model for authentication"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Hash and set the user password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the password against the stored hash"""
        return check_password_hash(self.password_hash, password)


class AuthenticationLog(Base):
    """Authentication log model to track login attempts"""
    __tablename__ = 'authentication_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    username = Column(String(80), nullable=False)
    attempt_type = Column(String(20), nullable=False)  # 'login', 'logout', 'failed_login'
    success = Column(Boolean, default=False)
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AuthenticationLog {self.username} - {self.attempt_type} at {self.timestamp}>'


class Session(Base):
    """Session model for user session management"""
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    token = Column(String(255), unique=True, nullable=False, index=True)
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    last_activity = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Session user_id={self.user_id} - active={self.is_active}>'


# Database configuration
DATABASE_URL = 'sqlite:///./password_manager.db'  # Change to your database URL


def get_db_engine(database_url=DATABASE_URL):
    """Create and return database engine"""
    return create_engine(database_url, echo=False)


def get_session_factory(database_url=DATABASE_URL):
    """Create and return session factory"""
    engine = get_db_engine(database_url)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db(database_url=DATABASE_URL):
    """Initialize database tables"""
    engine = get_db_engine(database_url)
    Base.metadata.create_all(bind=engine)
