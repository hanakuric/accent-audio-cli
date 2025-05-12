import os
import subprocess
import imageio_ffmpeg as ffmpeg_exe

def extract_audio(video_path: str, output_dir: str = None) -> str:
    """
    Extracts audio from the video file using a bundled FFmpeg (via imageio-ffmpeg).
    Returns the path to the .mp3 file.
    """
    if output_dir is None:
        output_dir = os.path.dirname(video_path)
    os.makedirs(output_dir, exist_ok=True)

    base = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(output_dir, f"{base}_audio.mp3")

    # Get the path to the static FFmpeg binary
    ffmpeg_path = ffmpeg_exe.get_ffmpeg_exe()

    # Build the command to extract a 16kHz mono MP3
    cmd = [
        ffmpeg_path,
        "-i", video_path,
        "-ac", "1",
        "-ar", "16000",
        "-vn",
        "-y",            # overwrite output if exists
        audio_path
    ]

    # Run FFmpeg
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        err = proc.stderr.decode(errors="ignore")
        raise Exception(f"FFmpeg extraction failed:\n{err}")
    return audio_path
