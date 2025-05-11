import os
import ffmpeg

def extract_audio(video_path: str, output_dir: str = None) -> str:
    """
    Extracts the audio track from a video file 
    """
    if output_dir is None:
        output_dir = os.path.dirname(video_path)
    os.makedirs(output_dir, exist_ok=True)

    base = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(output_dir, f"{base}_audio.mp3")

    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, format="mp3", acodec="libmp3lame", ac=1, ar="16000")
            .overwrite_output()
            .run(quiet=True)
        )
    except ffmpeg.Error as e:
        raise Exception(f"FFmpeg extraction failed: {e}")
    return audio_path
