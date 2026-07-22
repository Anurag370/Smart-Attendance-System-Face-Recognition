import insightface
from insightface.app import FaceAnalysis
import numpy as np
from functools import lru_cache
from app.config import settings

class FaceEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return 
        self._initialized = True

        print("="*50)
        print(f"Loading InsightFace Model: {settings.model_name}")
        self.app = FaceAnalysis(name=settings.model_name)
        self.app.prepare(ctx_id=settings.ctx_id, det_size=settings.det_size)
        print("Model Loaded successfully")
        print("="*50)

    def detect_faces(self, image:np.ndarray):
        return self.app.get(image)
    
    def get_embedding(self, image: np.ndarray) -> np.ndarray:
        faces = self.detect_faces(image)

        if len(faces) == 0:
            raise ValueError("No face detected")
        if len(faces) > 1:
            raise ValueError(f"Multiple faces detected: {len(faces)}")
        
        return faces[0].embedding
    

@lru_cache
def get_face_engine()-> FaceEngine:
    return FaceEngine()