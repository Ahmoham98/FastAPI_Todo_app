from core.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Boolean, Column, Integer, String, 
    DateTime, func, ForeignKey
)

class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True, default="")
    is_done = Column(Boolean, default=False)

    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    user = relationship("UserModel", back_populates="tasks", uselist=False)
    
    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, title={self.title!r}, is_done={self.is_done!r})"