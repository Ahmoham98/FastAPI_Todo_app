from fastapi import APIRouter, Path, Depends, HTTPException, status, Query

from core.tasks.schema import TaskCreateSchema, TaksResposeSchema, TaskUpdateSchema
from core.tasks.models import TaskModel
from core.users.models import UserModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.core.database import get_db
from core.core.pagination import PaginationParams, apply_pagination
from core.core.security import get_current_user

from typing import List

router = APIRouter(prefix="/todo", tags=["tasks"])


@router.get("/tasks", response_model=List[TaksResposeSchema])
async def retrieve_tasks_list(
    completed: bool = Query(
        None, description="filter tasks base on if they are completed"
    ),
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    # If user not active
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please varify your account first...",
        )

    # Getting all tasks for current user
    statement = select(TaskModel).where(TaskModel.user_id == current_user.id)

    # filters resluts if we had completed Query
    if completed is not None:
        statement = statement.where(TaskModel.is_done == completed)

    # Applying pagination for getting items from database
    statement = apply_pagination(statement, pagination)

    result = await db.execute(statement)
    return result.scalars().all()


@router.get("/tasks/{task_id}", response_model=TaksResposeSchema)
async def retrieve_task_detail(
    task_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    # Checking tasks ownership for current user
    statement = select(TaskModel).where(
        TaskModel.id == task_id, TaskModel.user_id == current_user.id
    )
    result = await db.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.post(
    "/tasks", response_model=TaksResposeSchema, status_code=status.HTTP_201_CREATED
)
async def inserts_new_task(
    task_data: TaskCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    # creating task with direct connection to current user id
    new_task = TaskModel(**task_data.model_dump(), user_id=current_user.id)
    db.add(new_task)
    # You can do flush when id needed
    await db.flush()
    await db.refresh(new_task)
    return new_task


@router.put("/tasks/{task_id}", response_model=TaksResposeSchema)
async def updates_task_data(
    task_data: TaskUpdateSchema,
    task_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    # Users updates it's own tasks only
    statement = select(TaskModel).where(
        TaskModel.id == task_id, TaskModel.user_id == current_user.id
    )
    result = await db.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    # Updating data for received task
    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    await db.flush()
    await db.refresh(task)
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletes_task(
    task_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    # Users can only delete their own tasks
    statement = select(TaskModel).where(
        TaskModel.id == task_id, TaskModel.user_id == current_user.id
    )
    result = await db.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    await db.delete(task)
    return None
