import os
import subprocess

def extract_frames_fast(stream_url: str,sf1f:str,vid:str):
    """
    Uses a single, efficient FFmpeg command to extract frames every 10 seconds.
    
    Args:
        stream_url: The direct video stream URL.
    """
    output_dir = vid
    os.makedirs(output_dir, exist_ok=True)
    print(f"Directory '{output_dir}' created. Starting FAST frame extraction...")

    command = [
        'ffmpeg',
        '-i', stream_url,                     # Input from the direct stream URL
        '-vf', 'fps=1/60',                    # The filter to apply: 1 frame every 10 seconds
        f'{output_dir}/frame_%04d.jpg'         # The output file pattern
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
