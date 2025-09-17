from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from core.api.chat.router import chat_router
from core.api.process_video.router import process_video
from core.lib.db import initialize_supabase
from dotenv import load_dotenv

load_dotenv()

BASE_PATH = "/core/v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: Database connections
    print("Application startup")
    await initialize_supabase()

    yield
    print("Application shutdown")
    

app = FastAPI(
    title="YT_RAG core api",
    description="API service for YT_RAG",
    vesrion="0.0.0",
    lifespan=lifespan,
)


# Todo: Add middleware
# app.add_middleware(
    
# )

app.include_router(chat_router, prefix=f"{BASE_PATH}/chat")
app.include_router(process_video, prefix=f"{BASE_PATH}/video")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)