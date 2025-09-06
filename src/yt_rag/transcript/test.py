from yt_rag.transcript.chunking import get_transcript_chunks

chunks = get_transcript_chunks(
    youtube_url="https://youtu.be/EIMmeR82FSw?feature=shared",
    chunk_duration=200,
    overlap_entires=5
)

for i, chunk in enumerate(chunks):
    print(f"""
          Chunk {i} : {chunk["page_content"][:50]} :\n
          metadata: {chunk["metadata"]["start"]}          
          
          """)