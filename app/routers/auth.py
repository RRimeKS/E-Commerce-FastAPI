from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.schemas.user import UserResponse, UserRegister, UserLogin
from app.models.user import User
from app.database import get_db
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.dependencies import isAuthentication
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=409, detail= "Email already registered")
    
    if db.query(User).filter(User.userName == user.userName).first():
        raise HTTPException(status_code=409, detail="Username already taken")

    user_data = User(
        firstName = user.firstName,
        lastName = user.lastName,
        userName = user.userName,
        email = user.email,
        password = hash_password(user.password),
        role = "user",
    )

    db.add(user_data)
    db.commit()
    db.refresh(user_data)

    return user_data

@router.post("/login")
async def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    existingUser = db.query(User).filter(
        or_(User.email == user.identifier, User.userName == user.identifier)
    ).first()

    if not existingUser or not verify_password(user.password, existingUser.password):
        raise HTTPException(status_code=401, detail="Email or password is wrong")

    token = create_access_token({"sub": str(existingUser.id)})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.JWT_EXPIRE_MINUTES * 60,
    )

    return {"message": "Login successful", "token": token}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(isAuthentication)):
    return current_user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}
