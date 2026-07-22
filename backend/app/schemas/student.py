from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class StudentCreate(BaseModel):
    student_id:str = Field(...,min_length=3, max_length=100, pattern=r"^[A-Z0-9-]+$")
    first_name:str = Field(..., min_length=1, max_length=100)
    last_name:str = Field(..., min_length=1, max_length=100)
    email:EmailStr
    department: Optional[str] = Field(None, max_length=100)

class StudentResponse(BaseModel):
    id:int
    student_id:str
    first_name:str
    last_name:str
    email:str
    department:str
    is_active:bool
    created_at:datetime

    class config:
        from_attributes = True