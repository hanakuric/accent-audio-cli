import os
from yt_dlp import YoutubeDL
from tqdm import tqdm
import requests
import re

VIDEO_EXTS = ("mp4", "mov", "webm", "m4v", "mpeg", "mpg")

def download_video(url: str, output_dir: str = "downloads") -> str:
    """
    Download any video URL 
    """
    os.makedirs(output_dir, exist_ok=True)

    if re.search(r"\.(" + "|".join(VIDEO_EXTS) + r")(\?.*)?$", url, re.IGNORECASE):
        local_fname = url.split("?")[0].rsplit("/", 1)[-1]
        out_path = os.path.join(output_dir, local_fname)
        resp = requests.get(url, stream=True, timeout=10)
        resp.raise_for_status()
        ctype = resp.headers.get("Content-Type", "")
        if not ctype.startswith("video/"):
            raise Exception(f"URL does not point to video (Content-Type={ctype})")
        total = int(resp.headers.get("Content-Length", 0))
        with open(out_path, "wb") as f, tqdm(
            total=total, unit="B", unit_scale=True, desc="Downloading"
        ) as pbar:
            for chunk in resp.iter_content(8192):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
        return out_path

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(id)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
