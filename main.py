from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import User
from schemas import LoginRequest, TokenResponse
from auth import verify_password, create_access_token
from routers import tickets

app = FastAPI(title="CopierMaster – Support System")

Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user.email,
        "role": user.role
    })

    return {"access_token": token}

app.include_router(tickets.router)
