import os
import datetime
import click

from accent_classify.downloader import download_video
from accent_classify.audio_extractor import extract_audio
from accent_classify.classifier import classify_accent

@click.command()
def main():
    """CLI: download video → extract audio → classify accent (audio‐only)."""
    click.echo("Video Accent Classification Tool (audio‐only)")
    click.echo("Enter a video URL or 'exit' to quit.")

    while True:
        url = click.prompt("Video URL", default="", show_default=False)
        if not url or url.lower() in {"exit", "quit"}:
            click.echo("Goodbye!")
            break

        try:
            click.echo("Downloading…")
            vid = download_video(url)
            click.echo(f"Downloaded → {vid}")
        except Exception as e:
            click.secho(f"Download error: {e}", fg="red")
            continue

        try:
            click.echo("Extracting audio…")
            aud = extract_audio(vid)
            click.echo(f"Extracted → {aud}")
        except Exception as e:
            click.secho(f"Audio extraction error: {e}", fg="red")
            continue

        try:
            click.echo("Classifying accent…")
            accent, confidence, explanation = classify_accent(aud)
            click.echo("Classification complete.\n")
        except Exception as e:
            click.secho(f"Classification failed: {e}", fg="red")
            continue

        click.secho("Accent:", bold=True);     click.echo(accent)
        click.secho("Confidence:", bold=True); click.echo(f"{confidence}%")
        click.secho("Explanation:", bold=True); click.echo(explanation)

        if click.confirm("\nSave report?", default=True):
            os.makedirs("reports", exist_ok=True)
            stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join("reports", f"report_{stamp}.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"Video URL: {url}\n\n")
                f.write(f"Accent: {accent}\n")
                f.write(f"Confidence: {confidence}%\n")
                f.write(f"Explanation: {explanation}\n")
            click.echo(f"Report saved → {path}")

        if not click.confirm("\nProcess another video?", default=False):
            click.echo("Goodbye!")
            break
        click.echo("\n" + "-"*40 + "\n")

if __name__ == "__main__":
    main()
