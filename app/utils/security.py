from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated
from passlib.context import CryptContext
from ..models.User import User, UserInDB
from ..schema.schemas import list_serial, serialize_for_model
from ..models.Token import Token, TokenData
from ..config.Config import collection_name
from fastapi.security import OAuth2PasswordBearer
import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv("SECRET_KEY_TIL")
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(email: str) -> Optional[UserInDB]:
    user = collection_name.find_one({"email": email})
    if user:
        user = serialize_for_model(user)
        return UserInDB(**user)
    return None

def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        username = payload.get("sub")
        email: str = payload.get("email")
        user_id: str = payload.get("user_id")
        if username is  None or email is None or user_id is None:
            raise credentials_exception
        token_data = TokenData(username=username, email=email, user_id=user_id)
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user(email)
    if user is None:
        raise credentials_exception
    return user