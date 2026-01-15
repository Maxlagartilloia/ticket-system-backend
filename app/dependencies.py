from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import os

from app.database import get_db
from app.models import User

# =========================
# CONFIG
# =========================

# Estas variables SE DEFINEN EN RENDER (Environment Variables)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in environment variables")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# =========================
# GET CURRENT USER
# =========================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


# =========================
# ROLE GUARDS
# =========================
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user


def require_supervisor(current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "supervisor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Supervisor privileges required"
        )
    return current_user


def require_technician(current_user: User = Depends(get_current_user)):
    if current_user.role != "technician":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Technician privileges required"
        )
    return current_user
