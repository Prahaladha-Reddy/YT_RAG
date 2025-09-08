from yt_rag.llm_service.gemini_with_memory import ChatGemini
from yt_rag.processors import process_youtube_video
from vector_store.vector_search import qdrant_search
from yt_rag.vector_store.embeddings import create_text_embeddings
from yt_rag.llm_service.cleaningextracted_data import extractchunk, extractimagename, image2bytes_converter

class RAGPipeline:
    def __init__(self, video_url):
        self.video_url = video_url
        self.video_id = None
    
    async def process_video(self):
        self.video_id = await process_youtube_video(self.video_url)
        return self.video_id
    
    def query_video(self, query, collection_name=None, embeddings=None):
        embeddings_in_sameclass = create_text_embeddings(query)
        effective_collection_name = collection_name if collection_name else self.video_id
        effective_embeddings = embeddings if embeddings else embeddings_in_sameclass
        retrieved_frames_metadata, retrieved_transcript_metadata = qdrant_search(
            collection_name=effective_collection_name, 
            query_embedding=effective_embeddings
        )
        image_paths = extractimagename(retrieved_frames_metadata)
        self.chunks = extractchunk(retrieved_transcript_metadata)
        self.image_bytes = image2bytes_converter(image_paths)
        return self.image_bytes, self.chunks
    
    async def query_gemini(self, query, collection_name=None, embeddings=None):
        image_bytes, chunks = self.query_video(query, collection_name, embeddings)
        response = await ChatGemini(query, image_bytes)
        return response.text
    
    async def chatgemini(self, prompt):
        response = await ChatGemini(prompt)
        return response.text
