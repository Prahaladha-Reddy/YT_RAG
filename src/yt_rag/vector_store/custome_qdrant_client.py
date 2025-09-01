from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

load_dotenv()


def get_qdrant():
  qdrant_client = QdrantClient(
      url=os.getenv('qdrant_URL'), 
      api_key=os.getenv('qdrant_KEY'),
  )
  return qdrant_client

