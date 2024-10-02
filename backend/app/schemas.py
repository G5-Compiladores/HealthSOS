from pydantic import BaseModel
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class HealthForm(BaseModel):
    alergias: bool | None
    alergias_medicamentos: bool | None
    medicamentos_actuales: str | None
    diabetes: bool | None
    marcapasos: bool | None
    epilepsia: bool | None
    grupo_sanguineo: str | None
    enfermedades_cardiacas: bool | None
    enfermedades_respiratorias: bool | None

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: str | None
    password: str | None

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True


class HealthFormResponse(BaseModel):
    message: str

class ChatbotQuestion(BaseModel):
    question: str

class ChatbotResponse(BaseModel):
    response: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)