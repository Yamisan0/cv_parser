from typing import Union

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    token: str
    token_type: str = "bearer"




##########################CV##########################

class CVBase(BaseModel):
    filename: str
    file_path: str

class CVCreate(CVBase):
    pass

class CV(CVBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

