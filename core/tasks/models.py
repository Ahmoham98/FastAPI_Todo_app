from core.database import Base
from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, func


class TaskModel(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    description = Column(Text(500), nullable=True ,default="")
    is_done = Column(Boolean,default=False)

    created_date = Column(DateTime, server_default=func.now())
    created_date = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    
    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, title={self.title!r}, is_done={self.is_done!r})"