from fastapi import APIRouter, Depends, HTTPException, status

from users.models import UserModel
from users.schema import (
    UserRegisterSchema,
    UserLoginSchema,
    TokenResponseSchema,
    RefreshTokenSchema
)

from core.database import get_db
from core.security import (
    create_access_token,
    create_refresh_token, 
    verify_token
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
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
    await db.refresh(user_obj)

    return {"detail": "User registered successfully"}

@router.post("/login", response_model=TokenResponseSchema)
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

    token_data = {"sub": str(user.id)}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh-token", response_model=TokenResponseSchema)
async def refresh_access_token(
    request: RefreshTokenSchema,
    db: AsyncSession = Depends(get_db)
):
    payload = verify_token(request.refresh_token, expected_type="refresh")

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    # Checking if user still exists
    # if you are using UUID, there is no need for int() in int(user_id_str) part of database query we are executing
    result = await db.execute(select(UserModel).where(UserModel.id == int(user_id_str)))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    # Token Rotation
    token_data = {"sub": str(user.id)}
    new_access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }






