# voice_api.py

import subprocess
from pathlib import Path
import os
import shutil
import tempfile
import re
from typing import Any, Dict, List, Optional

import torch
import torchaudio
import requests
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from transformers import AutoModel
from normalizer_multi import normalize_text  # you already have this

# Basic config
RASA_REST_URL = os.getenv(
    "RASA_REST_URL",
    "http://127.0.0.1:5005/webhooks/rest/webhook"
)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TTS_DIR = os.path.join(BASE_DIR, "tts_responses")  # where actions.py writes mp3s

# Hindi number conversion

HINDI_NUMBER_MAP = {
    'एक': 1, 'दो': 2, 'तीन': 3, 'चार': 4, 'पांच': 5,
    'छह': 6, 'छ': 6, 'सात': 7, 'आठ': 8, 'नौ': 9, 'दस': 10,

    'ग्यारह': 11, 'बारह': 12, 'तेरह': 13, 'चौदह': 14, 'पंद्रह': 15,
    'सोलह': 16, 'सत्रह': 17, 'अठारह': 18, 'उन्नीस': 19, 'बीस': 20,

    'तीस': 30, 'चालीस': 40, 'पचास': 50, 'साठ': 60, 'सत्तर': 70,
    'अस्सी': 80, 'नब्बे': 90,

    'सौ': 100, 'हज़ार': 1000, 'हजार': 1000, 'लाख': 100000
}


def convert_hindi_numbers_to_digits(text: str) -> str:
    """
    Convert Hindi number words to digits where possible.
    """
    if not text:
        return text

    original_text = text

    pattern1 = r'(एक|दो|तीन|चार|पांच|पाँच|छः|छह|छ|सात|आठ|नौ|दस|[०-९]+)\s*(हज़ार|हजार|सौ|लाख)'

    def replace_match(match):
        num_part = match.group(1)
        multiplier_part = match.group(2)

        devanagari_to_arabic = {
            '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
            '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
        }

        if any(c in devanagari_to_arabic for c in num_part):
            num_part = ''.join(devanagari_to_arabic.get(c, c) for c in num_part)
            base_num = int(num_part)
        else:
            base_num = HINDI_NUMBER_MAP.get(num_part, 1)

        multiplier = HINDI_NUMBER_MAP.get(multiplier_part, 1)

        result = base_num * multiplier
        return str(result)

    text = re.sub(pattern1, replace_match, text, flags=re.IGNORECASE)

    for hindi_word, digit in HINDI_NUMBER_MAP.items():
        if hindi_word in ['हज़ार', 'हजार', 'सौ', 'लाख']:
            continue
        text = re.sub(r'\b' + re.escape(hindi_word) + r'\b', str(digit), text, flags=re.IGNORECASE)

    if text != original_text:
        print(f"[HINDI_CONVERTER] '{original_text}' → '{text}'")

    return text


# FastAPI app

app = FastAPI(title="SahaYaa Voice Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for local demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expose generated TTS files
if os.path.isdir(TTS_DIR):
    app.mount(
        "/tts_responses",
        StaticFiles(directory=TTS_DIR),
        name="tts_responses"
    )

# ASR model

print("[VOICE_API] Using device:", DEVICE)
print("[VOICE_API] Loading IndicConformer...")

asr_model = AutoModel.from_pretrained(
    "ai4bharat/indic-conformer-600m-multilingual",
    trust_remote_code=True
).to(DEVICE)

FFMPEG_BIN = os.getenv("FFMPEG_PATH", "ffmpeg")


# Audio preprocessing

def ensure_wav_16k(input_path: str) -> str:
    """
    Make sure audio is mono 16kHz WAV; convert with ffmpeg if needed.
    """
    p = Path(input_path)

    if p.suffix.lower() == ".wav":
        return str(p)

    out_path = p.with_suffix(".wav")

    cmd = [
        FFMPEG_BIN,
        "-y",
        "-i", str(p),
        "-ac", "1",
        "-ar", "16000",
        str(out_path),
    ]

    try:
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"[FFMPEG] Converted {p} -> {out_path}")
    except Exception as e:
        print("[FFMPEG ERROR]", e)
        raise RuntimeError(f"Failed to convert {input_path} to wav") from e

    return str(out_path)


# ASR

def run_asr(audio_path: str, lang_code: str) -> Dict[str, Any]:
    """Run IndicConformer and return raw + normalized text."""
    wav_path = ensure_wav_16k(audio_path)

    wav, sr = torchaudio.load(wav_path)
    wav = torch.mean(wav, dim=0, keepdim=True)

    target_sample_rate = 16000
    if sr != target_sample_rate:
        resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=target_sample_rate)
        wav = resampler(wav)

    wav = wav.to(DEVICE)

    raw_text = asr_model(wav, lang_code, "rnnt")
    norm_text = normalize_text(raw_text, lang_code)

    return {
        "raw": raw_text,
        "normalized": norm_text,
    }


# Rasa bridge

def call_rasa(text: str, lang: str, sender: str = "cust_demo") -> List[Dict[str, Any]]:
    """Send one turn to Rasa REST channel and return its messages."""
    payload = {
        "sender": sender,
        "message": text,
        "metadata": {
            "lang": lang,
            "auth": {
                "user_id": sender,
                "biometric_score": 0.92,
                "liveness_passed": True,
                "otp_verified": False,
                "channel": "voice",
                "risk_label": "low",
            },
        },
    }
    print("[VOICE_API] Sending to Rasa:", payload)

    resp = requests.post(RASA_REST_URL, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()


# Response extraction

def extract_bot_and_audio(rasa_messages: List[Dict[str, Any]]) -> Dict[str, Optional[str]]:
    """Pick first bot text and any audio reply info from Rasa messages."""
    bot_text = None
    audio_url = None

    for msg in rasa_messages:

        if bot_text is None and "text" in msg:
            bot_text = msg["text"]

        custom = msg.get("custom")
        if not custom:
            custom = msg.get("data")
        if not custom:
            custom = msg.get("json")
        if not isinstance(custom, dict):
            continue

        if custom.get("type") == "audio_reply":
            audio_path = custom.get("audio_file")
            if audio_path:
                rel = audio_path.replace("\\", "/")
                if not rel.startswith("/"):
                    rel = "/" + rel
                audio_url = rel

    return {"bot_text": bot_text, "audio_url": audio_url}


# Main endpoint

@app.post("/api/voice-query")
async def voice_query(
    file: UploadFile = File(...),
    lang: str = Form("hi"),
    sender_id: str = Form("cust_demo"),
) -> Dict[str, Any]:
    """
    Full pipeline: audio -> ASR -> Rasa -> TTS (path).
    """
    suffix = ".wav" if file.filename.endswith(".wav") else ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        asr_out = run_asr(tmp_path, lang)
        raw = asr_out["raw"]
        norm = asr_out["normalized"]
        print("\n[ASR] RAW TEXT:", raw)
        print("[ASR] NORMALIZED TEXT:", norm)

        converted_text = convert_hindi_numbers_to_digits(norm)
        print("[CONVERTED] TEXT:", converted_text)

        rasa_msgs = call_rasa(converted_text, lang, sender=sender_id)
        print("[RASA] RESPONSES:", rasa_msgs)

        extracted = extract_bot_and_audio(rasa_msgs)

        return {
            "user_text": converted_text,
            "bot_text": extracted["bot_text"],
            "audio_url": extracted["audio_url"],
            "lang": lang,
        }
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass


# Health check

@app.get("/")
async def health_check():
    """Basic readiness probe for the voice gateway."""
    return {
        "status": "ok",
        "service": "SahaYaa Voice Gateway",
        "device": DEVICE,
        "rasa_url": RASA_REST_URL
    }
