from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import bcrypt
import os

DATABASE_URL = os.environ["DATABASE_URL"]

app = FastAPI(title="CopierMaster – Sistema de Soporte")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    correo: str
    password: str

@app.get("/")
def health():
    return {"status": "Backend activo"}

@app.post("/login")
def login(data: LoginRequest):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("""
            SELECT u.id, u.password_hash, r.nombre
            FROM usuarios u
            JOIN roles r ON u.rol_id = r.id
            WHERE u.correo = %s
        """, (data.correo,))

        user = cur.fetchone()
        conn.close()

        if not user:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")

        user_id, password_hash, rol = user

        if not bcrypt.checkpw(
            data.password.encode("utf-8"),
            password_hash.encode("utf-8")
        ):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")

        return {
            "status": "ok",
            "user_id": str(user_id),
            "rol": rol
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
