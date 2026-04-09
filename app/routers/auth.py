from fastapi import APIRouter, HTTPException, Depends, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.schemas.user import UserResponse, UserRegister, UserLogin
from app.models.user import User
from app.database import get_db
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.dependencies import isAuthentication
from app.config import settings
from app.limiter import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
@limiter.limit("5/minute")
async def register(request: Request, user: UserRegister, db: Session = Depends(get_db)):
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
@limiter.limit("5/minute")
async def login(request: Request, user: UserLogin, response: Response, db: Session = Depends(get_db)):
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
@limiter.limit("50/minute")
async def get_me(request: Request, current_user: User = Depends(isAuthentication)):
    return current_user

@router.post("/logout")
@limiter.limit("5/minute")
async def logout(response: Response, request: Request):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}