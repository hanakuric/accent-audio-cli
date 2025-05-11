import os
import torch
from transformers import pipeline

_PIPELINE = None
def _get_pipeline():
    global _PIPELINE
    if _PIPELINE is None:
        _PIPELINE = pipeline(
            "audio-classification",
            model="dima806/english_accents_classification",
            trust_remote_code=True,  
            top_k=1,
            device=0 if torch.cuda.is_available() else -1
        )
    return _PIPELINE

_LABEL_MAP = {
    "us": "American",
    "england": "British",
    "indian": "Indian",
    "australia": "Australian",
    "canada": "Canadian",
}

def classify_accent(audio_path: str):
    """
    Classify the speaker’s accent from raw audio.
    """
    pipe = _get_pipeline()
    results = pipe(audio_path)
    if not results:
        return "Unknown", 0, "The speaker uses unclear accent patterns."

    best = results[0]
    raw_label = best["label"].lower()
    accent = _LABEL_MAP.get(raw_label, raw_label.capitalize())
    confidence = int(best["score"] * 100)
    explanation = f"The speaker uses acoustic patterns typical of the {accent} accent."
    return accent, confidence, explanation
