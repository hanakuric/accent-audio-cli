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
    with st.spinner("Downloading video…"):
        video_path = download_video(url, output_dir=tempfile.mkdtemp())
    with st.spinner("Extracting audio…"):
        audio_path = extract_audio(video_path)
    with st.spinner("Classifying accent…"):
        accent, confidence, explanation = classify_accent(audio_path)

    st.success("Done!")
    st.subheader("Results")
    st.write(f"**Accent:** {accent}")  
    st.write(f"**Confidence:** {confidence}%")  
    st.write(f"**Explanation:** {explanation}")

    report = f"""Video URL: {url}
Accent: {accent}
Confidence: {confidence}%
Explanation: {explanation}
"""
    st.download_button(
        label="⬇️ Download Report",
        data=report,
        file_name="accent_report.txt",
        mime="text/plain"
    )
