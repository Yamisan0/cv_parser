from fastapi import FastAPI
# from models import User
# from database import SessionLocal
from routers import users
from routers import cv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



app.include_router(users.router, prefix="/auth", tags=["auth"])
app.include_router(cv.router, prefix='/cv', tags=["cv"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)