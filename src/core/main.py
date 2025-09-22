from contextlib import asynccontextmanager
from typing import Any, Dict
from core.lib.auth import get_supabase_client, verify_current_user
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import AsyncClient
import uvicorn
import asyncio
import sys
from dotenv import load_dotenv
from core.api.chat.router import chat_router
from core.api.process_video.router import video_router

load_dotenv()

BASE_PATH = "/core/v1"


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


app = FastAPI(
    title="YT_RAG core api",
    description="API service for YT_RAG",
    vesrion="0.0.0",
)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "UPDATE", "DELETE"],
    allow_headers=["*"]
)

@app.get(f"{BASE_PATH}/health")
def health_check():
    return {"status":"ok"}


@app.get(f"{BASE_PATH}/check_auth")
async def check_supabase(
    user: Dict[str, Any] = Depends(verify_current_user),
    supabse: AsyncClient = Depends(get_supabase_client)
):
    # print(user)
    return {
        "user": user
    }
    
app.include_router(router=chat_router, prefix=f"{BASE_PATH}/chat")
app.include_router(router=video_router, prefix=f"{BASE_PATH}/video")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)