from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import Usuario
from .auth import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    data = decode_token(token)
    user = db.query(Usuario).filter(Usuario.id == data["user_id"]).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return user


def require_roles(*roles):
    def role_checker(user=Depends(get_current_user)):
        if user.rol not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No autorizado"
            )
        return user
    return role_checker
