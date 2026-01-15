from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.models import Usuario
from app.auth import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(Usuario).filter(Usuario.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token(user.id, user.rol)

    return {
        "access_token": token,
        "token_type": "bearer",
        "rol": user.rol
    }
