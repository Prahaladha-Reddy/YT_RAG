from typing import Literal
from pydantic import BaseModel, Field

class ProcessVideoRequest(BaseModel):
    video_id: str

class ProcessedVideo(BaseModel):
    id: str
    created_at: str
    updated_at: str
    video_id: str
    video_title: str
    status: Literal["IDLE", "PROCESSING", "READY", "FAILED"]
    
class ProcessVideoResponse(BaseModel):
    success: str | None
    error: str | None
    
class VideoStatusRequest(BaseModel):
    video_id: str

class VideoStatusResponse(BaseModel):
    message: str
    is_processed: bool