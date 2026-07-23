from sqlalchemy import Column, Integer, LargeBinary, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Embedding(Base):
    __tablename__ = 'embeddings'
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    embedding_vector = Column(LargeBinary, nullable=False)  # 2048 bytes
    model_name = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    student = relationship(
        "Student",
        back_populates="embeddings"
    )