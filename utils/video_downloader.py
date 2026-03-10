import os
import subprocess
import sys

def download_video(video_url, output_dir="input_videos", filename="video.mp4"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    
    print(f"Downloading video from: {video_url}")
    
    command = [
        sys.executable, "-m", "yt_dlp",
        "-f", "bestvideo[vcodec^=avc1][ext=mp4]+bestaudio[ext=m4a]/mp4",
        "--merge-output-format", "mp4",
        "-o", output_path,
        video_url
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"✅ Video downloaded to: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ Error downloading video: {e}")
        return None
