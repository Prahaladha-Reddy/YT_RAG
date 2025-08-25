from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

load_dotenv()


def get_qdrent():
  qdrant_client = QdrantClient(
      url=os.getenv('QDRENT_URL'), 
      api_key=os.getenv('QDRENT_KEY'),
  )
  return qdrant_client

