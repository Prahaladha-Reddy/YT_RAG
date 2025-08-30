import yt_dlp

def get_video_info(youtube_url: str) -> dict:
    """
    Takes a YouTube URL and returns a dictionary containing the direct
    video stream URL and the video's duration in seconds.
    """
    ydl_opts = {'format': 'best[ext=mp4]'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        stream_url = info['url']
        duration = int(info['duration'])
        print(f"Successfully found stream URL for a video of {duration} seconds.")
        return {'stream_url': stream_url, 'duration': duration}