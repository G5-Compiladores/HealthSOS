from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User  # Import the SQLAlchemy User model
from PIL import Image
import qrcode
import io
from fastapi.responses import StreamingResponse

# FastAPI instance
app = FastAPI()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# QR code generation for user health information
@app.get("/generate_qr/{user_id}")
async def generate_qr(user_id: int, db: Session = Depends(get_db)):
    # Retrieve the user by ID from the database
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create the vCard or custom health information text
    health_info = f"""Health Information:
    Email: {user.email}
    Alergias: {"Sí" if user.alergias else "No"}
    Alergias a medicamentos: {"Sí" if user.alergias_medicamentos else "No"}
    Medicamentos actuales: {user.medicamentos_actuales}
    Diabetes: {"Sí" if user.diabetes else "No"}
    Marcapasos: {"Sí" if user.marcapasos else "No"}
    Epilepsia: {"Sí" if user.epilepsia else "No"}
    Grupo sanguíneo: {user.grupo_sanguineo}
    Enfermedades cardíacas: {"Sí" if user.enfermedades_cardiacas else "No"}
    Enfermedades respiratorias: {"Sí" if user.enfermedades_respiratorias else "No"}
    """

    # Create a QR code with the user's health information
    qr = qrcode.QRCode(
        version=3, 
        box_size=10, 
        border=5, 
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr.add_data(health_info)
    qr.make(fit=True)

    # Create the image for the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Optionally, add a logo to the QR code
    try:
        logo = Image.open("logo.png")
        logo = logo.resize((50, 50))

        img_w, img_h = img.size
        logo_w, logo_h = logo.size
        pos = ((img_w - logo_w) // 2, (img_h - logo_h) // 2)
        img.paste(logo, pos)
    except FileNotFoundError:
        # If the logo is not found, proceed without it
        pass

    # Save the QR code to a byte stream to return it as a response
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    # Return the QR code image as a response
    return StreamingResponse(img_byte_arr, media_type="image/png")
