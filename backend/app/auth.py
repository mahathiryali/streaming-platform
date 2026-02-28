from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import timezone, timedelta, datetime
import os
from dotenv import load_dotenv
import secrets

load_dotenv()

myctx = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
BCRYPT_MAX_CHARS = 72

def hash_password(password: str):
    safe_password = password[:BCRYPT_MAX_CHARS]
    return myctx.hash(safe_password)

def verify_password(password: str, hashed_password: str):
    safe_password = password[:BCRYPT_MAX_CHARS]
    return myctx.verify(safe_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta, token_type: str):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta 
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": token_type,
        "jti": secrets.token_hex(16)
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None 

def decode_access_token(token: str):
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        return None
    return payload

def decode_refresh_token(token: str):
    payload = decode_token(token)
    if payload is None or payload.get("type") != "refresh":
        return None
    return payload
