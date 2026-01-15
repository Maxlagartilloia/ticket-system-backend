from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt

SECRET_KEY = "copiermaster_tickets_secret_2026_seguro"
ALGORITHM = "HS256"

security = HTTPBearer()


def require_roles(*roles):
    def checker(token=Depends(security)):
        try:
            payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("rol") not in roles:
                raise HTTPException(status_code=403, detail="No autorizado")
            return payload
        except Exception:
            raise HTTPException(status_code=401, detail="Token inválido")
    return checker
