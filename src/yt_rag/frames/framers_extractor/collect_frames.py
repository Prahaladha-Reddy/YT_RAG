from yt_rag.frames.framers_extractor.ffmpeg_frame_extraction import extract_frames_fast
from yt_rag.frames.framers_extractor.yt_dlp_video_info import get_video_info

import re
class FrameCollector:
    def __init__(self, youtube_url: str, frame_interval: int = 20):

        self.youtube_url = youtube_url
        self.frame_interval = frame_interval
    def get_video_id(self)  :
        YT_ID_RE = re.compile(r'(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})')
        m = YT_ID_RE.search(self.youtube_url)
        return m.group(1) if m else None

    def run(self):
        self.video_id=self.get_video_id()
        print(f"starting frame extraction for video ID: {self.video_id}")
        video_info = get_video_info(self.youtube_url)
        if not video_info or 'stream_url' not in video_info:
            print(f"Could not retrieve video info for {self.youtube_url}. Aborting.")
            return

        stream_url = video_info['stream_url']
        print("successfully retrieved video stream URL.")

        print(f"extracting one frame every {self.frame_interval} seconds...")
        extract_frames_fast(
            stream_url=stream_url,
            vid=self.video_id
        )
        print("process complete")
        return self.video_id