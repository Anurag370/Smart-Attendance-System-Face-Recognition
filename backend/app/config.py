from pydantic_settings import BaseSettings
from typing import Tuple

class Settings(BaseSettings):
    database_url:str = "sqlite://./data/attendance.db"

    model_name:str = "buffalo_l"
    ctx_id:int = -1
    det_size:Tuple[int, int] = (640, 640)

    similarity_threshold:float = 0.40   

    camera_index:int = 1
    frame_width:int = 640
    frame_height:int = 640
    frame_skip:int = 3

    recognition_cooldown_seconds:int = 300
    late_cutoff_time:str = "08:30"

    log_level:str = "INFO"

    class Config:
        env_file  = ".env"


settings = Settings()