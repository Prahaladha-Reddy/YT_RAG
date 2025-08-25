from yt_rag.framers_extractor.collect_frames import FrameCollector
from yt_rag.vector_store.qdrent_vector_store import QdrantVectorStore
from pathlib import Path

def list_images(dir_path: str):
    p = Path(dir_path)
    exts = ("*.jpg", "*.jpeg", "*.png", "*.webp")
    files = [f.resolve() for pattern in exts for f in p.glob(pattern)]
    return sorted(files)  


class CollectPushandSearch:

  def __init__(self,youtube_url):
    self.youtube_url=youtube_url

  def collectframes(self):
    collctor=FrameCollector(youtube_url=self.youtube_url)
    self.video_id=collctor.run()
    self.images_path=f"./{self.video_id}"
    self.images=list_images(self.images_path)

    return self.images,self.video_id
  
  def pushframes(self):
    self.vector_store = QdrantVectorStore()

    was_successful = self.vector_store.add_images(
    collection_name=self.video_id,
    image_paths=self.images,
    video_id=self.video_id
  )
    return was_successful
  

  def search(self,query,collection_name):
    results = self.vector_store.search(
    collection_name=collection_name,
    query=query
    )
    return results
     