import os
from moviepy.editor import VideoFileClip

def extract_audio(video_path: str, output_dir: str = None) -> str:
    """
    Extract audio 
    """
    if output_dir is None:
        output_dir = os.path.dirname(video_path)
    os.makedirs(output_dir, exist_ok=True)

    base = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(output_dir, f"{base}_audio.mp3")

    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, codec="libmp3lame")
    clip.close()

    return audio_path
