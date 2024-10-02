from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    alergias = Column(Boolean)
    alergias_medicamentos = Column(Boolean)
    medicamentos_actuales = Column(String)
    diabetes = Column(Boolean)
    marcapasos = Column(Boolean)
    epilepsia = Column(Boolean)
    grupo_sanguineo = Column(String)
    enfermedades_cardiacas = Column(Boolean)
    enfermedades_respiratorias = Column(Boolean)