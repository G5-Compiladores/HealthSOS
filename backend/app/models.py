from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base  # Ensure this is relative if in the same package

# User table
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

    # Establish a one-to-many relationship with the QRCode table
    qr_codes = relationship("QRCode", back_populates="user")

# QRCode table
class QRCode(Base):
    __tablename__ = "qr_codes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    qr_code_data = Column(String, nullable=False)  # Store the QR code data as a string (could be a URL or encoded data)

    # Relationship with User table
    user = relationship("User", back_populates="qr_codes")


