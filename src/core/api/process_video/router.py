from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from supabase import AsyncClient

from core.api.process_video.models import ProcessVideoRequest, ProcessVideoResponse, VideoStatusRequest, VideoStatusResponse
from core.lib.db import get_supabase_client

video_router = APIRouter()

video_router.post("/process_video")
async def process_video(
    request: ProcessVideoRequest,
    # user: Dict[str, any] = Depends(verify_user_access)
    supabase: AsyncClient = Depends(get_supabase_client)
):
    return ProcessVideoResponse(
        success = f"{request.video_id} processed successfully"
    )
    
    
@video_router.get("/video_status")
async def get_video_status(
    video_id: str,
    supabase: AsyncClient = Depends(get_supabase_client)
):
    return VideoStatusResponse(
        message = f"{video_id} is already processed",
        is_processed = False
    )