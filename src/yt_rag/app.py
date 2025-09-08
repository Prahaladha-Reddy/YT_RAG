from yt_rag.main import RAGPipeline
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
import asyncio
import sys, asyncio
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(
    title="RAG Pipeline API",
    description="An API to process YouTube videos and query them using   a RAG pipeline.",
    version="1.0.0"
)

#pipeline_storage: Dict[str, RAGPipeline] = {}

class ProcessRequest(BaseModel):
    video_url: str = Field(..., description="The URL of the YouTube video to process.")

class QueryRequest(BaseModel):
    video_id: str = Field(..., description="The ID of the processed video to query.")
    query: str = Field(..., description="The question or query for the RAG pipeline.")

class ChatRequest(BaseModel):
    prompt: str = Field(..., description="A general prompt for the chat model (no RAG).")


@app.post("/process/",status_code=202)
async def process_video(request:ProcessRequest):
    pipeline= RAGPipeline(request.video_url)
    video_id=await pipeline.process_video()


"""
@app.post("/process/", status_code=202)
async def process_video(request: ProcessRequest):
    try:
        pipeline = RAGPipeline(video_url=request.video_url)
        await asyncio.to_thread(pipeline)  
        if pipeline.video_id:
            pipeline_storage[pipeline.video_id] = pipeline
            return {
                "message": "Video processing initiated successfully.",
                "video_id": pipeline.video_id
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to extract video ID during processing.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during video processing: {e}")

@app.post("/query/")
async def query_processed_video(request: QueryRequest):
    pipeline = pipeline_storage.get(request.video_id)
   
    if not pipeline:
        raise HTTPException(
            status_code=404,
            detail=f"Video ID '{request.video_id}' not found. Please process it first using the /process/ endpoint."
        )
   
    try:
        response = await pipeline.query_gemini(query=request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during querying: {e}")

@app.post("/chat/")
async def chat_without_rag(request: ChatRequest):

    try:
        dummy_pipeline = RAGPipeline(video_url=None)
        response = await dummy_pipeline.chatgemini(prompt=request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred in the chat endpoint: {e}") """