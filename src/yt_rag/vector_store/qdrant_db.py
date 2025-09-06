import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

def get_qdrant_client():

    qdrant_client = QdrantClient(
        url = os.getenv('MINE_QDRANT_URL'),
        api_key = os.getenv("MINE_QDRANT_KEY")
    )

    return qdrant_client