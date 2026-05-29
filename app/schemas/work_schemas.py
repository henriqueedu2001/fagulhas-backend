from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from fastapi import UploadFile

class RegisterWorkRequest(BaseModel):
    title: str
    date: datetime
    isbn: Optional[str]
    pages_num: int

class RegisterWorkResponse(BaseModel):
    work_id: int
    edition_id: int

class GeneralResponse(BaseModel):
    message: str

