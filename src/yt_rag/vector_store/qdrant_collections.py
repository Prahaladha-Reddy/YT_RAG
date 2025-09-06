import logging
import uuid
from yt_rag.vector_store.qdrant_db import get_qdrant_client
from qdrant_client.models import PointStruct, VectorParams, Distance, PayloadSchemaType

logger = logging.getLogger(__name__)


def upsert_images_to_collection(
    collection_name: str,
    embeddings: list,
    images_metadata: list,
    video_id: str
):
    """
    Upsert image embeddings to a Qdrant collection.
    """
    try:
        client = get_qdrant_client()
        
        if collection_name in [collection.name for collection in client.get_collections().collections]:
            logger.info(f"Collection exists: {collection_name}")
            points = [
                PointStruct(
                    id = images_metadata[idx]["id"],
                    vector = {"image_vector": embedding},
                    payload = {
                        "video_id": video_id,
                        "type": "image",
                        "path": images_metadata[idx]["path"]
                    }
                    
                ) for idx, embedding in enumerate(embeddings)
            ]

            client.upsert(collection_name=collection_name, points=points)
            return True
        else:
            logger.info(f"Create a collection: {collection_name}")
            client.create_collection(
                collection_name=collection_name,
                vectors_config={
                    "text_vector": VectorParams(size=512, distance=Distance.COSINE),
                    "image_vector": VectorParams(size=512, distance=Distance.COSINE)
                }
            )
            
            
            # Add payload index for filtering
            client.create_payload_index(
                collection_name=collection_name,
                field_name="type",
                field_schema=PayloadSchemaType.KEYWORD,
            )

            points = [
                PointStruct(
                    id = images_metadata[idx]["id"],
                    vector = {"image_vector": embedding},
                    payload = {
                        "video_id": video_id,
                        "type": "image",
                        "path": images_metadata[idx]["path"]
                    }
                    
                ) for idx, embedding in enumerate(embeddings)
            ]

            client.upsert(collection_name=collection_name, points=points)
            return True

    except Exception as e:
        logger.error(f"Failed to upsert images to collection: {e}")
        return False

def upsert_transcript_chunks_to_collection(
    collection_name: str, 
    embeddings: list, 
    transcript_metadata: list, 
    video_id: str
):
    try:
        client = get_qdrant_client()

        if collection_name in [collection.name for collection in client.get_collections().collections]:
            logger.info(f"Collection exists: {collection_name}")
            points = [
                PointStruct(
                    id = transcript_metadata[idx]["id"],
                    vector = {"text_vector": embedding},
                    payload = {
                        "video_id": video_id,
                        "type": "text",
                        "start_time": transcript_metadata[idx]["start"],
                        "metadata": transcript_metadata[idx]
                    },
                    
                )
                for idx, embedding in enumerate(embeddings)
            ]
            
            client.upsert(collection_name=collection_name, points=points)
            return True
        else:
            client.create_collection(
                collection_name=collection_name,
                vectors_config={
                    "text_vector":VectorParams(size=512, distance=Distance.COSINE),
                    "image_vector": VectorParams(size=512, distance=Distance.COSINE)
                }
            )
            
            # Add payload index for filtering
            client.create_payload_index(
                collection_name=collection_name,
                field_name="type",
                field_schema=PayloadSchemaType.KEYWORD,
            )

            logger.info(f"Create a collection: {collection_name}")
            points = [
                PointStruct(
                    id = transcript_metadata[idx]["id"],
                    vector = {"text_vector": embedding},
                    payload = {
                        "video_id": video_id,
                        "type": "text",
                        "start_time": transcript_metadata[idx]["start"],
                        "metadata": transcript_metadata[idx]
                    }
                )
                for idx, embedding in enumerate(embeddings)
            ]
            
            client.upsert(collection_name=collection_name, points=points)
            return True
    except Exception as e:
        logger.error(f"Failed to upsert transcript chunks to collection: {e}")
        return False