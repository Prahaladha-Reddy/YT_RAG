import asyncio
import logging
import uuid
import json
from typing import List, Optional, Tuple, Dict, Any
import traceback
from yt_rag.transcript.chunking import get_transcript_chunks
from yt_rag.frames.collect_frames import collect_frames_from_ffmpeg
from yt_rag.vector_store.embeddings import create_image_embeddings, create_text_embeddings_batch
from yt_rag.vector_store.qdrant_collections import upsert_images_to_collection, upsert_transcript_chunks_to_collection
from yt_rag.helper.get_id_from_youtube_url import get_video_id

DEFAULT_CHUNK_DURATION = 50
DEFAULT_OVERLAP_ENTRIES = 5

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
async def extract_video_content(youtube_url: str):
    """
    Extract transcript chunks and video frames in parallel from a YouTube video
    """
    transcript_chunks = None
    image_folder_path = None
    images_metadata = None
    
    try:
        logger.info(f"Starting content extraction for video: {youtube_url}")
        
        # Transcript extraction
        try:
            logger.info("Starting transcript extraction...")
            transcript_chunks = await get_transcript_chunks(
                youtube_url=youtube_url,
                chunk_duration=DEFAULT_CHUNK_DURATION,
                overlap_entires=DEFAULT_OVERLAP_ENTRIES  # Fixed typo
            )
            logger.info(f"Transcript extraction completed: {len(transcript_chunks) if transcript_chunks else 0} chunks")
        except Exception as e:
            logger.error(f"Transcript extraction failed: {e}")
            logger.error(f"Transcript traceback: {traceback.format_exc()}")
        
        # Frames extraction (runs regardless of transcript success/failure)
        try:
            logger.info("Starting frames extraction...")
            image_folder_path, images_metadata = await asyncio.to_thread(
                collect_frames_from_ffmpeg,
                youtube_url=youtube_url
            )
            logger.info(f"Frames extraction completed: {len(images_metadata) if images_metadata else 0} frames")
        except Exception as e:
            logger.error(f"Frames extraction failed: {e}")
            logger.error(f"Frames traceback: {traceback.format_exc()}")
        
        logger.info(f"Content extraction summary - Transcript chunks: {len(transcript_chunks) if transcript_chunks else 0}, "
                   f"Frames: {len(images_metadata) if images_metadata else 0}")
        
        return transcript_chunks, image_folder_path, images_metadata
    
    except Exception as e:
        logger.error(f"Unexpected error in extract_video_content for {youtube_url}: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return transcript_chunks, image_folder_path, images_metadata

async def process_image_embeddings(video_id: str, images_metadata: List[str]) -> bool:
    """
    Process and store image embeddings in the vector database.
    """
    try:        
        images_path = [image["path"] for image in images_metadata]
        
        # Create image embeddings
        image_embeddings = create_image_embeddings(images_path)
        
        # Store embeddings in vector database
        upsert_images_to_collection(
            collection_name=video_id,
            embeddings=image_embeddings,
            images_metadata=images_metadata,
            video_id=video_id
        )
        
        logger.info(f"Successfully processed and stored {len(images_path)} image embeddings")
        return True
        
    except Exception as e:
        logger.error(f"Error processing image embeddings: {e}")
        return False


async def process_text_embeddings(video_id: str, transcript_chunks: List[Dict]) -> bool:
    """
    Process and store text embeddings from transcript chunks in the vector database.
    """
    try:        
        texts_to_embed = [chunk["page_content"] for chunk in transcript_chunks]
        
        text_embeddings = create_text_embeddings_batch(texts_to_embed)
        
        transcript_metadata = [{
            "id": chunk["id"],
            "start": chunk["metadata"]["start"],
            "page_content": chunk["page_content"]
        } for chunk in transcript_chunks]
        
        # store embeddings in vector database
        upsert_transcript_chunks_to_collection(
            collection_name=video_id,
            embeddings=text_embeddings,
            transcript_metadata=transcript_metadata,
            video_id=video_id
        )
        
        logger.info(f"Successfully processed and stored {len(transcript_chunks)} text embeddings")
        return True
        
    except Exception as e:
        logger.error(f"Error processing text embeddings: {e}")
        return False


async def process_youtube_video(youtube_url: str):
    """
    Main function to process a YouTube video through the complete RAG pipeline.
    """
    try:
        video_id = get_video_id(youtube_url)
        
        # Extract video content (transcript and frames)
        transcript_chunks, images_folder_path, images_metadata = await extract_video_content(youtube_url)
        
        with open(f"transcript_{video_id}.json", "w", encoding="utf-8") as f:
            data = json.dumps(transcript_chunks, default=str)
            f.write(data)

        if images_metadata:
            await process_image_embeddings(video_id, images_metadata)
        else:
            logger.warning("No image frames extracted, skipping image processing")
        
        if transcript_chunks:
            await process_text_embeddings(video_id, transcript_chunks)
        else:
            logger.warning("No transcript chunks extracted, skipping text processing")
        
        return video_id
        
    except Exception as e:
        logger.error(f"Error in video processing pipeline: {e}")
        return False


async def main():
    
    youtube_url = "https://youtu.be/dZ19NAbUISs?si=8ZlJ5gbZsxmylOBG"
    
    logger.info("Starting YouTube RAG processing pipeline")
    success = await process_youtube_video(youtube_url)
    
    if success:
        logger.info("Video processing completed successfully!")
    else:
        logger.error("Video processing failed!")
        return 1
    
    return 0


if __name__ == "__main__":
    asyncio.run(main())