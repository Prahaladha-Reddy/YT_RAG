from yt_rag.frames.collect_frames import collect_frames_from_ffmpeg

folder_path = collect_frames_from_ffmpeg(
    youtube_url="https://www.youtube.com/watch?v=wn-tTeOmVRE",
)

print(folder_path)