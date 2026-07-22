import os
import uuid
import cv2 as cv
import numpy as np
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import settings
from app.schemas.student import StudentCreate, StudentResponse
from app.repositories.student_repo import StudentRepository
from app.recognition.engine import get_face_engine, FaceEngine
from app.utils.image_utils import decode_image, is_blurry, crop_face

router = APIRouter(prefix="/api/v1/students", tags=["Students"])

@router.post("", response_model=dict, status_code=201)
async def register_student(
    student_id:str = Form(...),
    first_name:str = Form(...),
    last_name:str = Form(...),
    email:str = Form(...),
    department:str = Form(None),
    face_image: UploadFile = File(...),
    db:Session = Depends(get_db),
    engine:FaceEngine = Depends(get_face_engine)
    ):
    student_data = StudentCreate(
        student_id=student_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        department=department
    )

    repo = StudentRepository(db)

    if repo.get_by_student_id(student_id):
        raise HTTPException(409, detail={
            "error": "Duplicate Student Id",
            "message" : f"Student with id {student_id} alredy exists"
        })
    
    if repo.get_by_email(email):
        raise HTTPException(409, detail={
            "error":"Duplicate Email Id",
            "message":f"Student with {email} already exists"
        })
    
    image_bytes = await face_image.read()
    if len(image_bytes) == 0:
        raise HTTPException(400, detail={
            "error":"Empty Image",
            "message":"Uploded file is empty"
        })
    
    try:
        img = decode_image(image_bytes)
    except ValueError as e:
        raise HTTPException(400, detail={
            "error":"Corrputed image",
            "message":str(e)
        })
    
    faces = engine.detect_faces(img)

    if len(faces) == 0:
        raise HTTPException(400, detail={
            "error":"No face detected",
            "message":"No face found in the iamge"
        })
    
    if len(faces) > 1:
        raise HTTPException(400, detail={
            "error":"Multiple Faces",
            "message":f"Detected {len(faces)} faces, Please upload image with single face"
        })
    
    face = faces[0]

    face_region = crop_face(img, face.bbox)

    if is_blurry(face_region):
        raise HTTPException(400, detail={
            "error":"Blurred Face",
            "message":"Face is too blurry. Please use a sharper Image."
        })
    
    if face.det_score < 0.7:
        raise HTTPException(400, detail={
            "error":"Low Confidence",
            "message":f"Faces detection score is low: {face.det_score:.2f}"
        })
    
    os.makedirs("data/faces", exist_ok=True)
    filename = f"{student_id}_{uuid.uuid4().hex[:8]}.jpg"
    filepath = os.path.join("data", "faces", filename)
    cv.imwrite(filepath, face_region)

    db_student = repo.create({
        "student_id": student_data.student_id,
        "first_name": student_data.first_name,
        "last_name": student_data.last_name,
        "email": student_data.email,
        "department": student_data.department,
        "face_image_path": filepath
    })

    return {
        "id": db_student.id,
        "student_id": db_student.student_id,
        "first_name": db_student.first_name,
        "last_name": db_student.last_name,
        "email": db_student.email,
        "message": "Student registered successfully"
    }