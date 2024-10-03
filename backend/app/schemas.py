from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Optional

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Schema for the health form information
class HealthForm(BaseModel):
    alergias: Optional[bool] = None
    alergias_medicamentos: Optional[bool] = None
    medicamentos_actuales: Optional[str] = None
    diabetes: Optional[bool] = None
    marcapasos: Optional[bool] = None
    epilepsia: Optional[bool] = None
    grupo_sanguineo: Optional[str] = None
    enfermedades_cardiacas: Optional[bool] = None
    enfermedades_respiratorias: Optional[bool] = None

    class Config:
        from_attributes = True  # Changed from 'orm_mode' to 'from_attributes'


# Base user schema
class UserBase(BaseModel):
    email: str

    class Config:
        from_attributes = True  # Changed from 'orm_mode' to 'from_attributes'


# Schema for creating a new user
class UserCreate(UserBase):
    password: str


# Schema for updating user information
class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True  # Changed from 'orm_mode' to 'from_attributes'


# Schema representing a user retrieved from the database
class User(UserBase):
    id: int


# Schema for QR code information
class QRCodeSchema(BaseModel):
    user_id: int
    qr_code_data: str

    class Config:
        from_attributes = True  # Changed from 'orm_mode' to 'from_attributes'


# Password hashing and verification methods
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


### Key Points:
# - **HealthForm**: Captures the health-related data for each user.
# - **UserCreate**: Used for creating a new user, includes `password`.
# - **UserUpdate**: Allows partial updates to the user's email and password.
# - **QRCodeSchema**: Captures the `user_id` and the corresponding `qr_code_data`, which will be generated and stored in the database.
# This setup should work seamlessly with your FastAPI app, SQLAlchemy models, and QR code generation logic.###