from pydantic import BaseModel

# ---------- AUTH ----------

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ---------- TICKETS ----------

class TicketCreate(BaseModel):
    institution: str
    equipment: str
    description: str
    priority: str

class TicketResponse(TicketCreate):
    id: int
    status: str
    technician: str | None

    class Config:
        orm_mode = True
