from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from users.schema import UserRegisterSchema, UserLoginSchema
from users.models import UserModel
from core.database import get_db

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register")
async def user_register(
    request: UserRegisterSchema, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(UserModel).where(UserModel.email == request.email.lower()))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username already exists",
        )

    user_obj = UserModel(email=request.email.lower())
    user_obj.hash_password(request.password)

    db.add(user_obj)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"detail": "user registered successfully"}
    )

@router.post("/login")
async def user_login(
    request: UserLoginSchema, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(UserModel).where(UserModel.email == request.email.lower()))
    user = result.scalar_one_or_none()

    if user is None or not user.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={"detail": "Login successful"}
    )





