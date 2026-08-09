from fastapi import APIRouter, Path, Depends, HTTPException, status

from tasks.schema import TaskCreateSchema, TaksResposeSchema, TaskUpdateSchema
from tasks.models import TaskModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import get_db

from typing import List

router = APIRouter(prefix="/todo", tags=["tasks"])

@router.get("/tasks", response_model=List[TaksResposeSchema])
async def retrieve_tasks_list(db: AsyncSession = Depends(get_db)):
    statement = select(TaskModel)
    result = await db.execute(statement)
    return result.scalars().all()

@router.get("/tasks/{task_id}", response_model=TaksResposeSchema)
async def retrieve_task_detail(task_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)):
    statement = select(TaskModel).where(TaskModel.id == task_id)
    result = await db.execute(statement)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.post("/tasks", response_model=TaksResposeSchema, status_code=status.HTTP_201_CREATED)
async def inserts_new_task(task_data: TaskCreateSchema, db: AsyncSession = Depends(get_db)):
    new_task = TaskModel(**task_data.model_dump())
    db.add(new_task)
    # You can do flush when id needed
    await db.flush() 
    await db.refresh(new_task)
    return new_task

@router.put("/tasks/{task_id}", response_model=TaksResposeSchema)
async def updates_task_data(task_data: TaskUpdateSchema, task_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)):
    statement = select(TaskModel).where(TaskModel.id == task_id)
    result = await db.execute(statement)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    # Updating data for received task
    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    
    await db.flush()
    await db.refresh(task)
    return task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletes_task(task_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)):
    statement = select(TaskModel).where(TaskModel.id == task_id)
    result = await db.execute(statement)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    await db.delete(task)
    return None

