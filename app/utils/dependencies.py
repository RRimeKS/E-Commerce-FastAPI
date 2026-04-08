from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.database import get_db
from app.utils.security import decode_access_token

def isAuthentication(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def require_role(*roles: str):
    def role_checker(currentUser: User = Depends(isAuthentication)):
        if currentUser.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return currentUser
    return role_checker