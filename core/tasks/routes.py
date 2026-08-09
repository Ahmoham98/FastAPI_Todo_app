from fastapi import APIRouter

router = APIRouter(prefix="/todo", tags=["tasks"])

@router.get("/tasks")
async def retrieve_tasks_list():
    return {}

@router.get("/tasks/{task_id}")
async def retrieve_task_detail(task_id: int):
    return {}

@router.post("/tasks")
async def retrieve_task_detail(task_id: int):
    return {}

@router.put("/tasks/{task_id}")
async def retrieve_task_detail(task_id: int):
    return {}

@router.delete("/tasks/{task_id}")
async def retrieve_task_detail(task_id: int):
    return {}

