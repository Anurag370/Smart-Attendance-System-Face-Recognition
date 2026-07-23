from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from app.models.embedding import Embedding
from app.models.student import Student
from typing import Optional


class EmbeddingRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, student_id: int, embedding_bytes: bytes, model_name: str) -> Embedding:
        emb = Embedding(
            student_id=student_id,
            embedding_vector=embedding_bytes,
            model_name=model_name
        )
        self.db.add(emb)
        self.db.commit()
        self.db.refresh(emb)
        return emb
    
    def get_by_student_id(self, student_id: int) -> Optional[Embedding]:
        return self.db.query(Embedding).filter(
            Embedding.student_id == student_id
        ).first()
    
    def get_all_embeddings(self) -> list[dict]:
        results = (
            self.db.query(
                Embedding.embedding_vector,
                Embedding.student_id
            )
            .join(Student, Student.id == Embedding.student_id)
            .filter(Student.is_active.is_(True))
            .all()
        )
        
        return [
            {
                'student_id': r.student_id,
                'embedding_bytes': r.embedding_vector
            }
            for r in results
        ]
    
    def delete_by_student_id(self, student_id: int) -> bool:
        count = self.db.query(Embedding).filter(
            Embedding.student_id == student_id
        ).delete()
        self.db.commit()
        return count > 0