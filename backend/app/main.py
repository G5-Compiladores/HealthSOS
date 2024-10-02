from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database
from . import auth

app = FastAPI()


@app.post("/register", response_model=schemas.UserCreate)
async def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(email=user.email, hashed_password=schemas.get_password_hash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not schemas.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/health-form", response_model=schemas.HealthForm)
async def submit_health_form(form: schemas.HealthForm, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    for key, value in form.dict().items():
        setattr(current_user, key, value)
    db.commit()
    return form


# Read
@app.get("/health-form", response_model=schemas.HealthForm)
async def read_health_form(current_user: models.User = Depends(auth.get_current_user)):
    return schemas.HealthForm(
        alergias=current_user.alergias,
        alergias_medicamentos=current_user.alergias_medicamentos,
        medicamentos_actuales=current_user.medicamentos_actuales,
        diabetes=current_user.diabetes,
        marcapasos=current_user.marcapasos,
        epilepsia=current_user.epilepsia,
        grupo_sanguineo=current_user.grupo_sanguineo,
        enfermedades_cardiacas=current_user.enfermedades_cardiacas,
        enfermedades_respiratorias=current_user.enfermedades_respiratorias
    )

# Update
@app.put("/health-form", response_model=schemas.HealthForm)
async def update_health_form(form: schemas.HealthForm, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    for key, value in form.dict().items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return form

# Delete
@app.delete("/health-form", status_code=status.HTTP_204_NO_CONTENT)
async def delete_health_form(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    for field in schemas.HealthForm.__fields__:
        setattr(current_user, field, None)
    db.commit()
    return {"message": "Health form data deleted successfully"}

# Additional CRUD operations for user management

# Read all users (admin operation)
@app.get("/users", response_model=List[schemas.UserBase])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# Read a specific user
@app.get("/users/{user_id}", response_model=schemas.UserBase)
async def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Update a user
@app.put("/users/{user_id}", response_model=schemas.UserBase)
async def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

# Delete a user
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)