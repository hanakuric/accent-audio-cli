# Accent Audio Classification CLI

A simple, self-contained command-line tool that:

1. **Accepts** a public video URL (YouTube, Loom, direct MP4, etc.)
2. **Downloads** the video into `downloads/`
3. **Extracts** its audio track via FFmpeg
4. **Analyzes** the speaker’s English accent **directly from the audio waveform**
5. **Outputs**

   * **Accent** (e.g. American, British, Australian, etc.)
   * **Confidence** (0–100%)
   * **Explanation** (“The speaker uses …”)
6. **Optionally saves** a timestamped report in `reports/`

---

## Prerequisites

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git ffmpeg
```

### macOS (Homebrew)

```bash
brew install python git ffmpeg
```

### Windows (Chocolatey)

1. Open PowerShell **as Administrator**
2. Install Chocolatey (if you haven’t):

   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force
   [System.Net.ServicePointManager]::SecurityProtocol = 'Tls12'
   iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```
3. Install dependencies:

   ```powershell
   choco install python git ffmpeg -y
   ```
4. Restart your shell.

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-org/accent-cli.git
   cd accent-cli
   ```

2. **Create & activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # macOS/Linux
   venv\Scripts\activate         # Windows PowerShell
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```


## How to Run

With your virtual environment activated, run:

```bash
python main.py
# or
python3 main.py
````

1. **Enter** a video URL when prompted (or type `exit` to quit).
2. The script will:

   * Download the video (into `downloads/`)
   * Extract audio (`<video>_audio.mp3`)
   * Classify the accent from the audio
3. **Results** appear on-screen.
4. Choose whether to **save** a report (text file) under `reports/`.
5. Opt to **process another** URL or **exit**.

---

## Example Session

```bash
$ python main.py
Video URL: https://youtu.be/Qf0J6Ibbj-k
Downloading… → downloads/Qf0J6Ibbj-k.mp4
Extracting audio… → downloads/Qf0J6Ibbj-k_audio.mp3
Classifying accent…
Accent: British
Confidence: 88%
Explanation: The speaker uses acoustic patterns typical of the British accent.
Save report? [Y/n]: Y
Report saved → reports/report_20250511_174512.txt
Process another video? [y/N]: n
Goodbye!
```

---

## Project Structure

```
.
├── accent_classify/
│   ├── __init__.py
│   ├── downloader.py
│   ├── audio_extractor.py
│   └── classifier.py
├── downloads/               # downloaded videos
├── reports/                 # saved text reports
├── main.py                  # CLI entrypoint
├── requirements.txt
└── README.md
```

---

## Troubleshooting

* **`ffmpeg: command not found`**
  Install FFmpeg system-wide (`sudo apt install ffmpeg` / `brew install ffmpeg` / `choco install ffmpeg`).

* **Import errors in VS Code**
  Ensure VS Code’s Python interpreter is set to your project `venv/bin/python3` (or `venv\\Scripts\\python.exe`).

* **Video download failures**
  Try the shortened YouTube URL form (`https://youtu.be/...`) or a direct MP4 link.

---

