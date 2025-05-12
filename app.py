import os
import tempfile
import streamlit as st
from accent_classify.downloader import download_video
from accent_classify.audio_extractor import extract_audio
from accent_classify.classifier import classify_accent

st.set_page_config(page_title="Accent ID CLI", layout="centered")
st.title("🎤 Accent Audio Classification")
st.markdown("Paste a public video URL and click ▶️ to detect accent from the audio.")

url = st.text_input("Video URL (YouTube, Loom, MP4…)", "")
if st.button("▶️ Analyze Accent") and url:
    try:
        with st.spinner("Downloading video…"):
            tmpdir = tempfile.mkdtemp()
            video_path = download_video(url, output_dir=tmpdir)
        st.success(f"Downloaded → {os.path.basename(video_path)}")
    except Exception as e:
        st.error(f"❌ Download failed:\n{e}\n\nTry a different URL or a direct MP4 link.")
        st.stop()

    try:
        with st.spinner("Extracting audio…"):
            audio_path = extract_audio(video_path)
        st.success(f"Extracted → {os.path.basename(audio_path)}")
    except Exception as e:
        st.error(f"❌ Audio extraction failed:\n{e}")
        st.stop()

    try:
        with st.spinner("Classifying accent…"):
            accent, confidence, explanation = classify_accent(audio_path)
        st.success("Classification complete!")
    except Exception as e:
        st.error(f"❌ Classification failed:\n{e}")
        st.stop()

    st.subheader("Results")
    st.write(f"**Accent:** {accent}")  
    st.write(f"**Confidence:** {confidence}%")  
    st.write(f"**Explanation:** {explanation}")

    report = (
        f"Video URL: {url}\n"
        f"Accent: {accent}\n"
        f"Confidence: {confidence}%\n"
        f"Explanation: {explanation}\n"
    )
    st.download_button(
        label="⬇️ Download Report",
        data=report,
        file_name="accent_report.txt",
        mime="text/plain",
    )
