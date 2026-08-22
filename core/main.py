from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from tasks.routes import router as task_router
from users.routes import router as user_router

# Import Users to avoid circular import when define Table relationship 
from tasks.models import TaskModel
from users.models import UserModel

from core.security import get_current_user, get_current_user_from_cookie

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")

tags_metadata = [
    {
        "name": "tasks",
        "description": "Operations related to tasks. Create, read, update, and delete tasks.",
        "externalDocs": {
            "description": "Tasks External Documentation",
            "url": "https://example.com/docs/tasks",
        },
    },
    {
        "name": "users",
        "description": "Operations about users. Register, login, and profile management.",
    },
]
description = "You can simply clone the project, run fastapi dev and start developing your fastapi app using this template which also is easy to scale as your app goes to scale to" \
" become bigger as your files and folders grows. this template helps you to focus more on developement rather than taking time on arranging standard template for developing fastapi apps"
summary ="A clean template for start Developing FastAPI app"

app = FastAPI(
    title="LMS / Todo API",
    description=description,
    summary=summary,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Ahmad Mohammadzadeh",
        "url": "https://www.linkedin.com/in/ahmmad-mohammadzadeh",
        "email": "electricallover45@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

app.include_router(task_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")

@app.get("/", tags=["root"])
async def get_root():
    return {"detail": "Welcome to Todo app aplication!"}

@app.get("/public", tags=["main"])
async def test_public_root():
    return {"detail": "You have successfully connected to public route"}

@app.get("/private", tags=["main"])
async def get_authenticated_user(current_user: UserModel = Depends(get_current_user)):
    return {
        "detail": "Your have successfully connected to private route",
        "user_id": current_user.id,
        "user_is_active": current_user.is_active,
    }

@app.get("/private/from-cookie", tags=["main"])
async def get_authenticated_user_by_cookie(current_user: UserModel = Depends(get_current_user_from_cookie)):
    return {
            "detail": "Your have successfully connected to private route",
            "user_id": current_user.id,
            "user_is_active": current_user.is_active,
        }