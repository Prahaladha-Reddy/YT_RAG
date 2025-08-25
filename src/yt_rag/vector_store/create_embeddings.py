from yt_rag.vector_store.fast_embeddings import Embeddings

image_embeddings=Embeddings.Image_Embedding_model

text_embeddings=Embeddings.Text_Embedding_model

def create_image_embeddings(images):
  embeddings = list(image_embeddings.embed(images))
  return embeddings

def create_text_embeddings(query):
  embeddings=list(text_embeddings.embed([query]))
  return embeddings[0]