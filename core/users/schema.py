from pydantic import BaseModel, Field
from datetime import datetime

class TaskBaseSchema(BaseModel):
    title: str = Field(..., max_length=150, min_length=5, description="Title of the task")
    description: str | None = Field(None, max_length=500, description="Description of the task")
    is_done: bool = Field(default=False, description="State of the task")

class TaskCreateSchema(TaskBaseSchema):
    pass

class TaskUpdateSchema(TaskBaseSchema):
    # Rewrite title to be Optional
    title: str | None = Field(None, max_length=150, min_length=5, description="Title of the task")

class TaksResposeSchema(TaskBaseSchema):
    id: int = Field(..., description="Unique identifier of the object")
    
    created_date: datetime = Field(..., description="Creation date & time of the object")
    updated_date: datetime = Field(..., description="Updating date & time of the object")