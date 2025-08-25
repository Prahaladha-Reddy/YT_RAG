from yt_rag.vector_store.create_embeddings import create_text_embeddings, create_image_embeddings
from yt_rag.vector_store.vector_search import qdrent_search
from yt_rag.vector_store.qdrent_collections import upsert_to_collection

class QdrantVectorStore:
    def __init__(self):
        print("QdrantVectorStore initialized.")

    def add_images(self, collection_name: str, image_paths: list, video_id: str) -> bool:
        print(f"Creating embeddings for {len(image_paths)} images...")
        try:
            image_embeddings = create_image_embeddings(image_paths)
            if image_embeddings is False:
                raise ValueError("Embedding creation function returned False.")
            print("Embeddings created successfully.")
        except Exception as e:
            print(f"Failed to create image embeddings: {e}")
            return False

        print(f"Upserting to collection '{collection_name}'...")
        try:
            print("Entering the try block")
            success = upsert_to_collection(
                Collection_name=collection_name,
                embeddings=image_embeddings,
                images_collection=image_paths,
                video_id=video_id
            )

            return success
        except Exception as e:
            print(f"Upserting failed: {e}")
            return False

    def search(self, collection_name: str, query: str):

        print(f"Creating embedding for query: '{query}'...")
        try:
            query_embedding = create_text_embeddings(query)
            if query_embedding is False:
                raise ValueError("Query embedding creation returned False.")
            print("Query embedding created.")
        except Exception as e:
            print(f"Failed to create query embedding: {e}")
            return None

        print(f"Searching collection '{collection_name}'...")
        try:
            search_results = qdrent_search(
                query_embeddings=query_embedding,
                collection_name=collection_name
            )
            print("Search complete.")
            return search_results
        except Exception as e:
            print(f"Search failed: {e}")
            return None