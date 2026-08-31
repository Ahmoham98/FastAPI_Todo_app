from fastapi import FastAPI, Depends, status, HTTPException, Request
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from tasks.routes import router as task_router
from users.routes import router as user_router

# Import Users to avoid circular import when define Table relationship (Do not delete them)
from tasks.models import TaskModel
from users.models import UserModel, UserRole

from core.security import get_current_user, get_current_user_from_cookie
from core.config import settings
from core.dependencies import RoleChecker
from core.database import get_db
from core.seeder import seed_data
from core.middleware import setup_middlewares

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


# ---- Middleware and routes ----
setup_middlewares(app)

app.include_router(task_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
# ------------------------------

# ---- endpoints ----
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

@app.get("/check-role", tags=["main"])
async def check_user_role(current_user: UserModel = Depends(RoleChecker(allowed_roles=[UserRole.ADMIN, UserRole.USER]))):
    return {
        "detail": "Your have successfully connected to role-check route",
        "user_id": current_user.id,
        "user_role": current_user.role,
    }

@app.post("/seed-data", status_code=status.HTTP_201_CREATED, tags=['seed_data'])
async def trigger_seed_data(
    user_count: int = 5,
    tasks_per_user: int = 3,
    db: AsyncSession = Depends(get_db)
):
    """Inserts new data to database for developement 

    Args:
        user_count (int, optional): number of users you want it to insert to database. Defaults to 5.
        tasks_per_user (int, optional): number of tasks you want to insert to database per user. Defaults to 3.
    """
    if getattr(settings, "ENVIRONMENT", "development") == "production":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seeding data is not allowed in production environment."
        )

    result = await seed_data(db, user_count=user_count, tasks_per_user=tasks_per_user)
    return result
# ------------------------------

