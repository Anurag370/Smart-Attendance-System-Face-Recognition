from sqlalchemy.orm import Session
from app.models.student import Student
from typing import Optional

class StudentRepository:
    def __init__(self, db:Session):
        self.db = db

    def create(self, data: dict)-> Student:
        student = Student(**data)
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student
    
    def get_by_id(self, id:int) -> Optional[Student]:
        return self.db.query(Student).filter(Student.id == id).first()
    
    def get_by_student_id(self, student_id:str)->Optional[Student]:
        return self.db.query(Student).filter(Student.student_id == student_id).first()
    
    def get_by_email(self, email:str) -> Optional[Student]:
        return self.db.query(Student).filter(Student.email == email).first()
    
    def get_all_active(self, skip:int, limit:int = 100, department:str = None):# type: ignore
        query = self.db.query(Student).filter(Student.is_active == True)
        if department:
            query = query.filter(Student.department == department)
        return query.offset(skip).limit(limit).all()
    
    def count_active(self, department:str = None)->int:# type: ignore
        query = self.db.query(Student).filter(Student.is_active == True)
        if department:
            query = query.filter(Student.department == department)
        return query.count()
    
    def soft_delete(self, id:int)-> Optional[Student]:
        student = self.get_by_id(id)
        if student:
            student.is_active = False # type: ignore
            self.db.commit()
        return student
                
