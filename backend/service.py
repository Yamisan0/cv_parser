from passlib.context import CryptContext
from fastapi import HTTPException, Security
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from config import SECRET_KEY
from schemas import UserCreate, UserLogin
import jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return password_context.hash(password)

def get_user_cvs(db: Session, email: str):
    user = db.query(User).filter_by(email=email).one_or_none()
    if user is None:
        return None
    paths = [cv.file_path for cv in user.cv]
    # print(paths)  # Print paths to verify if they're fetched correctly
    return paths

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = {"email": data["email"]}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    res = {"token": encoded_jwt, "token_type": "bearer"}
    return res

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def authenticate_user(db: Session, username: str, password: str) -> bool:
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        return False
    if not verify_password(password, user.password):
        return False

    return True

def add_user(db: Session, user: UserCreate):
    if db.query(User).filter(User.email == user.email).first() or db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Email or username already registered")
    
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if not isinstance(new_user, dict):
        new_user = vars(new_user)

    return new_user

def login_user(db: Session, user: UserLogin):
    find_user = db.query(User).filter(User.email == user.email).first()

    if not find_user or not verify_password(plain_password=user.password, hashed_password=find_user.password):
        raise HTTPException(status_code=401, detail="Email or password doesn't exist")

    user_path = get_user_cvs(db, user.email) # test 

    user_data = {"email": find_user.email}  
    return create_access_token(user_data, expires_delta=timedelta(hours=1))
