from yt_rag.llm_service.gemini_with_memory import ChatGemini, clear_memory, get_memory_size, save_memory_to_file, load_memory_from_file
from yt_rag.processors import process_youtube_video
from yt_rag.vector_store.vector_search import qdrant_search
from yt_rag.vector_store.embeddings import create_text_embeddings
from yt_rag.llm_service.cleaningextracted_data import extractchunk, extractimagename, image2bytes_converter
from yt_rag.llm_service.system_prompt import system_prompt

class RAGPipeline:
    def __init__(self, video_url, memory_file="conversation_memory.json"):
        self.video_url = video_url
        self.video_id = None
        self.memory_file = memory_file
        self.conversation_memory = []

    async def process_video(self):
        """Process the YouTube video and extract its ID."""
        self.video_id = await process_youtube_video(self.video_url)
        if self.video_id:
            self.memory_file = f"conversation_memory_{self.video_id}.json"
        self.load_conversation_memory()
        return self.video_id

    def query_video(self, query, collection_name=None, embeddings=None):
        """Query the video content and retrieve relevant frames and transcript chunks."""
        embeddings_in_sameclass = create_text_embeddings(query)
        effective_collection_name = collection_name if collection_name else self.video_id
        effective_embeddings = embeddings if embeddings else embeddings_in_sameclass
        retrieved_frames_metadata, retrieved_transcript_metadata = qdrant_search(
            collection_name=effective_collection_name, 
            query_embedding=effective_embeddings
        )
        image_paths = extractimagename(retrieved_frames_metadata)
        chunks = extractchunk(retrieved_transcript_metadata)
        image_bytes = image2bytes_converter(image_paths)
        return image_bytes, chunks

    def query_gemini(self, query, collection_name=None, embeddings=None):
        """Query Gemini with video context and conversation memory."""
        image_bytes, chunks = self.query_video(query, collection_name, embeddings)
        retrieval_chunk = ""
        for conv in chunks:
            retrieval_chunk += conv
            retrieval_chunk += "\n"
        response = ChatGemini(
            prompt=query,
            system_prompt=system_prompt,
            images=image_bytes,
            use_memory=True,
            conversation_memory=self.conversation_memory
        )
        return response.text

    def chatgemini(self, prompt):
        """Chat with Gemini using conversation memory."""
        response = ChatGemini(
            prompt=prompt,
            system_prompt=system_prompt,
            images=None,
            use_memory=True,
            conversation_memory=self.conversation_memory
        )
        return response.text

    def clear_conversation_memory(self):
        """Clear the conversation memory."""
        clear_memory(self.conversation_memory)

    def get_conversation_memory_size(self):
        """Get the current number of messages in conversation memory."""
        return get_memory_size(self.conversation_memory)

    def save_conversation_memory(self):
        """Save the conversation memory to a JSON file."""
        save_memory_to_file(self.memory_file, self.conversation_memory)

    def load_conversation_memory(self):
        """Load conversation memory from a JSON file."""
        load_memory_from_file(self.memory_file, self.conversation_memory)