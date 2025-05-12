import os
import re
import requests
from yt_dlp import YoutubeDL
from tqdm import tqdm

VIDEO_EXTS = ("mp4", "mov", "webm", "m4v", "mpeg", "mpg")

def download_video(url: str, output_dir: str = "downloads") -> str:
    """
    Download any video URL into downloads
    """
    os.makedirs(output_dir, exist_ok=True)

    if re.search(r"\.(" + "|".join(VIDEO_EXTS) + r")(\?.*)?$", url, re.IGNORECASE):
        fname = url.split("?", 1)[0].rsplit("/", 1)[-1]
        out_path = os.path.join(output_dir, fname)
        resp = requests.get(url, stream=True, timeout=10)
        resp.raise_for_status()
        total = int(resp.headers.get("Content-Length", 0))
        with open(out_path, "wb") as f, tqdm(total=total, unit="B", unit_scale=True) as p:
            for chunk in resp.iter_content(8192):
                f.write(chunk); p.update(len(chunk))
        return out_path

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": os.path.join(output_dir, "%(id)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
