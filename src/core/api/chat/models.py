import datetime
from typing import Literal, Optional
from pydantic import BaseModel


class SampleMessage(BaseModel):
    content: str
    
class ChatRequest(BaseModel):
    videoId: str
    content: str

class ChatMessage(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    processed_video_id: datetime
    user_id: str
    role: Literal["ASSISTANT", "USER"]
    content: str
    metadata: dict | None