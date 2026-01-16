from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from app.database import get_db
from app import models, schemas
from app.dependencies import SECRET_KEY, ALGORITHM

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# =========================
# PASSWORD CONFIG
# =========================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


# =========================
# UTILS
# =========================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(user_id: int, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": user_id,
        "role": role,
        "exp": expire
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# =========================
# LOGIN
# =========================
@router.post(
    "/login",
    response_model=schemas.TokenResponse
)
def login(
    credentials: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(models.User.email == credentials.email)
        .first()
    )

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive"
        )

    access_token = create_access_token(
        user_id=user.id,
        role=user.role
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role
    }


# =========================
# CREATE FIRST ADMIN (ONE-TIME, SAFE)
# =========================
@router.post(
    "/bootstrap-admin",
    status_code=status.HTTP_201_CREATED
)
def bootstrap_admin(
    email: str,
    full_name: str,
    password: str,
    db: Session = Depends(get_db)
):
    # Si ya existe al menos un admin, el endpoint queda bloqueado
    existing_admin = (
        db.query(models.User)
        .filter(models.User.role == "admin")
        .first()
    )

    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bootstrap admin is disabled"
        )

    admin = models.User(
        email=email,
        full_name=full_name,
        hashed_password=get_password_hash(password),
        role="admin",
        is_active=True
    )

    db.add(admin)
    db.commit()

    return {
        "message": "Admin user created successfully"
    }
