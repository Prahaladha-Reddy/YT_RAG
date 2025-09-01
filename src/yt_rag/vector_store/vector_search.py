from yt_rag.vector_store.custome_qdrant_client import get_qdrant

def qdrant_search(collection_name,query_embeddings):

  client=get_qdrant()
  frames_metadata = []
  results = client.search(
    collection_name=collection_name,
    query_vector=query_embeddings,
    limit=2
    )
  
  for frame in results:
    frames_metadata.append(
        {"score":frame.score,
          "id":frame.id,
          "image_path":frame.payload['path'],
          "video_id":frame.payload['vid_id']
          }
    )

  return frames_metadata
  