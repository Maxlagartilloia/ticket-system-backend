from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database import get_db
from app import models, schemas
from app.dependencies import verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.TokenResponse)
def login(
    credentials: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    # 1. Buscar usuario por email (ADN del sistema)
    user = db.query(models.User).filter(
        models.User.email == credentials.email
    ).first()

    # 2. Validar existencia y contraseña usando la utilidad de dependencies
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Validar estado de la cuenta
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # 4. Generar Token JWT con el 'sub' y el 'role' (Standard Blueprint)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role
    }
