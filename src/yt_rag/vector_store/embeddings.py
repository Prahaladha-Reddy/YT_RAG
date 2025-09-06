from yt_rag.vector_store.fastembed_model import EmbedModels

image_embeddings=EmbedModels.Image_Embedding_model

text_embeddings=EmbedModels.Text_Embedding_model

def create_image_embeddings(images):
  embeddings = list(image_embeddings.embed(images))
  return embeddings

def create_text_embeddings(query):
  embeddings=list(text_embeddings.embed([query]))
  return embeddings[0]

def create_text_embeddings_batch(texts):
  """Create embeddings for multiple texts at once for better performance"""
  embeddings = list(text_embeddings.embed(texts))
  return embeddings