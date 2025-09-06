from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from yt_rag.helper.get_id_from_youtube_url import get_video_id


def fallback_transcript_extract(youtube_url: str):
    yt_api = YouTubeTranscriptApi()
    try:
        transcript_data = yt_api.fetch(
            video_id = get_video_id(youtube_url),
            languages = ("en", 'hi', "es", "de", "te")
        )
        
        transcript = format_fetched_transcript(transcript_data)
        return transcript
    except NoTranscriptFound as e:
        return []

def format_fetched_transcript(transcript_data):
    transcript = []
    for snippet in transcript_data.snippets:
        transcript.append({
            "text": snippet.text,
            "seconds": snippet.start
        })
    
    return transcript
        