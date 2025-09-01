from yt_rag.vector_store.custome_qdrant_client import get_qdrant
from qdrant_client.models import PointStruct, VectorParams, Distance


def upsert_to_collection(Collection_name,embeddings,images_collection,video_id):
  client=get_qdrant()
  print("Recieved clinet")

  if Collection_name in [collection.name for collection in client.get_collections().collections]:
    print(f"There is this collection {Collection_name}")
    points = [
      PointStruct(id=idx,
                  vector=embedding,
                  payload={"path": images_collection[idx],"vid_id":video_id})
      for idx, embedding in enumerate(embeddings)
    ]
    print("completed constructing points")

    client.upsert(collection_name=Collection_name, points=points)
    print("upserting completed")
  else:
    print(f"the collection with name is {Collection_name} not fond so creating one")
    client.create_collection(
        collection_name=Collection_name,
        vectors_config=VectorParams(size=512, distance=Distance.COSINE)
    )
    print(f"the collection with name is {Collection_name} has been created")

    points = [
      PointStruct(id=idx,
                  vector=embedding,
                  payload={"path": images_collection[idx],"vid_id":video_id})
      for idx, embedding in enumerate(embeddings)
    ]
    print("completed constructing points")

    client.upsert(collection_name=Collection_name, points=points)
    print("upserting completed")
