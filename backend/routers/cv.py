import json
from fastapi import APIRouter, Depends, UploadFile, HTTPException, Form, File
from typing import List
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from .users import oauth2_scheme
import shutil
from service import verify_token, get_db, get_user_cvs
from fastapi.responses import JSONResponse
from pathlib import Path
from config import UPLOAD_DIRECTORY
from models import User
import jwt
from sqlalchemy.orm import Session
from models import CV
import subprocess
from pydantic import BaseModel
import asyncio


class Ranking(BaseModel):
    rank: int
    file_path: str
    score: int
    alerteFort: bool


router = APIRouter()

BASE_DIR = Path("/uploads")

BASE_DIR.mkdir(parents=True, exist_ok=True)


#Ajouter cette partie au prototype de la fn
# , payload: dict = Depends(verify_token)
@router.post("/upload")
async def upload_pdf(files: List[UploadFile] = File(...),
                     payload: dict = Depends(verify_token),
                     db: Session = Depends(get_db)
                     ):
    print("Le payload est constitue de :", payload)
    email = payload["email"]

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_dir = Path(BASE_DIR) / user.username
    user_dir.mkdir(parents=True, exist_ok=True)

    for file in files:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        file_path = user_dir / file.filename

        with file_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)

        new_cv = CV(filename=file.filename, file_path=str(file_path), owner_id=user.id)
        db.add(new_cv)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "File uploaded successfully", "filename": file.filename})


@router.get("/rankings", response_model=List[Ranking])
async def get_rankings(payload: dict = Depends(verify_token),
                       db: Session = Depends(get_db)
                       ):

    resumes_path = ""

    all_cv_path = get_user_cvs(db, payload["email"])
    if all_cv_path:
        resumes_path = all_cv_path[0].rsplit('/', 1)[0]       #Not really efficient, not need to that a whole object for this
    else:
        resumes_path = "./resumes_pdf"

    script_path = "./scripts/abd_better_parse.py"
    keywords_path = "./scripts/yes.json"
    
    print("Executing script...")

    process = await asyncio.create_subprocess_exec(
        "python3", script_path, resumes_path, keywords_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    
    print("Script executed")
    if process.returncode != 0:
        print(f"Error: {stderr.decode()}")
        raise HTTPException(status_code=500, detail=f"Error executing script: {stderr.decode()}")

    try:
        output = stdout.decode()
        output = output[output.index('['):]
        rankings = json.loads(output)
    except ValueError as e:
        print(f"ValueError: {e}")
        raise HTTPException(status_code=500, detail="Script output is not valid JSON")
    
    return rankings