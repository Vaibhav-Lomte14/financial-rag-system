from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "mysecretkey"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict):

    expire = datetime.utcnow() + timedelta(hours=1)

    data.update({"exp": expire})

    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm="HS256"
    )