from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import models, database

# Secret key and algorithm for JWT
SECRET_KEY = "your_secret_key"  # Replace with a more secure key, e.g., from environment variables
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme for retrieving tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Function to create a JWT access token
def create_access_token(data: dict):
    to_encode = data.copy()
    # Set token expiration time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Encode the JWT token with secret and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to get the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    # Raise an exception if the credentials are invalid
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # Extract the subject (user email)
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Query the user from the database by email
    user = db.query(models.User).filter(models.User.email == email).first()
    
    # Raise an exception if the user does not exist
    if user is None:
        raise credentials_exception
    
    return user


# Optional: Function to get a token expiration time in minutes
def create_access_token_with_expiry(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

