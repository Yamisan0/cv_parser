from fastapi import APIRouter, Depends
from typing import Annotated, Union
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from service import add_user, login_user, verify_token
from database import SessionLocal
from schemas import UserCreate, UserLogin, UserResponse


router = APIRouter()

session = SessionLocal()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/signup", response_model=UserCreate)
async def create_account(user: UserCreate):
    new_user = add_user(session, user)
    return new_user

@router.post("/login", response_model=UserResponse)
async def login(user: UserLogin):
    user_log = login_user(session, user)
    print("Login route used ici!!!!")
    return user_log

@router.get("/user")
def get_user(payload: dict = Depends(verify_token)):
    return {"email": payload["email"], "message": "This is a protected route"}