import enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from pwdlib import PasswordHash
from core.core.database import Base

# Creates an object for hashing password
password_hash = PasswordHash.recommended()

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)

    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    tasks = relationship("TaskModel", back_populates="user")

    # Method for hashing password
    def hash_password(self, plain_password: str) -> str:
        """Hashes the given password using bcrypt."""
        self.password = password_hash.hash(plain_password)

    # Method for password validation
    def verify_password(self, plain_password: str) -> bool:
        """Verifies the given password against the stored hash."""
        return password_hash.verify(plain_password, self.password)