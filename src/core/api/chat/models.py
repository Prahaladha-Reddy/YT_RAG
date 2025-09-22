from datetime import datetime
from typing import Literal, Optional, List
from pydantic import BaseModel
import uuid


class ChatRequest(BaseModel):
    video_id: str
    query: str
class ChatResponse(BaseModel):
    content: str

class ChatMessage(BaseModel):
    id: uuid.UUID
    role: Literal["USER", "ASSISTANT"]
    content: str
    timestamp: datetime
    video_id: Optional[str] = None

class ChatHistoryRequest(BaseModel):
    video_id: str

class ChatHistoryResponse(BaseModel):
    history: List[ChatMessage]
