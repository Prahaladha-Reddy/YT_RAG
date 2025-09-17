from fastapi import APIRouter, HTTPException, Depends
from supabase import AsyncClient
from src.core.api.chat.models import ChatMessage, ChatRequest, SampleMessage
from src.core.lib.db import get_supabase_client

chat_router = APIRouter()

@chat_router.post("/generate")
async def generate_chat(
    request: ChatRequest,
    # user: Dict[str, Any] = Depends(verify_user_access);
    supabase: AsyncClient = Depends(get_supabase_client)
):
    # Logic to invoke LLM with RAG as tool to generate response
    return SampleMessage(
        content=f"Return API Chat sucess for Request {request.content}"
    )
    
    
