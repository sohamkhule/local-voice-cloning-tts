# tts_engine.py
import os
import shutil
import uuid
from functools import lru_cache
from pathlib import Path

import torch
from TTS.api import TTS

# Folders
VOICES_DIR = Path("voices")
OUTPUT_DIR = Path("generated_audios")
for d in (VOICES_DIR, OUTPUT_DIR):
    d.mkdir(exist_ok=True)

# Model
DEFAULT_MODEL_NAME = "tts_models/multilingual/multi-dataset/your_tts"

def _gpu_available() -> bool:
    """
    Check if CUDA or MPS (Apple Silicon) is available.
    """
    try:
        if torch.cuda.is_available():
            return True
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return True
        return False
    except Exception:
        return False

@lru_cache(maxsize=1)
def _get_tts():
    """
    Lazy-load and cache the TTS model for faster reuse.
    """
    use_gpu = _gpu_available()
    device_str = "GPU/MPS" if use_gpu else "CPU"
    print(f"[TTS] Loading model: {DEFAULT_MODEL_NAME} | Device={device_str}")
    return TTS(model_name=DEFAULT_MODEL_NAME, progress_bar=False, gpu=use_gpu)

def list_saved_voices():
    """
    List all saved voice profiles (without extension).
    """
    voices = ["Default (model voice)"]
    for p in sorted(VOICES_DIR.glob("*.wav")):
        voices.append(p.stem)
    return voices

def save_voice_profile(wav_path: str, profile_name: str) -> str:
    """
    Save uploaded/recorded sample in the voices/ directory.
    """
    safe = "".join(ch for ch in profile_name if ch.isalnum() or ch in ("_", "-")).strip("_-")
    if not safe:
        safe = f"profile_{uuid.uuid4().hex[:8]}"
    dst = VOICES_DIR / f"{safe}.wav"
    shutil.copy(wav_path, dst)
    return str(dst)

def _get_valid_language(tts, requested_lang: str) -> str:
    """
    Check if requested language is available, else fallback to first available.
    """
    available_langs = getattr(tts, "languages", None)
    if isinstance(available_langs, (list, dict)):
        if requested_lang in available_langs or (isinstance(available_langs, dict) and requested_lang in available_langs.keys()):
            return requested_lang
        fallback = list(available_langs)[0]
        print(f"[TTS] ⚠️ Requested language '{requested_lang}' not available. Using fallback: '{fallback}'")
        return fallback
    return requested_lang  # if model doesn't expose language list

def generate_tts(text: str, speaker_wav: str | None, file_name: str = "output.wav", language: str = "en") -> str:
    """
    Generate TTS audio to generated_audios/<file_name>.
    If speaker_wav is provided, use it for zero-shot cloning.
    """
    out_path = OUTPUT_DIR / file_name
    tts = _get_tts()

    # Ensure valid language
    language = _get_valid_language(tts, language)

    kwargs = dict(text=text, file_path=str(out_path), language=language)
    if speaker_wav and os.path.exists(speaker_wav):
        print(f"[TTS] Using speaker_wav: {speaker_wav}")
        kwargs["speaker_wav"] = speaker_wav
    elif speaker_wav:
        print(f"[TTS] ⚠️ speaker_wav not found at {speaker_wav}; using default voice.")

    tts.tts_to_file(**kwargs)
    return str(out_path)

if __name__ == "__main__":
    demo_text = "Hello! This is a quick test of the upgraded XTTS system."
    print(generate_tts(demo_text, None, "demo.wav", language="en"))










# # tts_engine.py
# import os
# import shutil
# import uuid
# from functools import lru_cache
# from pathlib import Path

# import torch
# from TTS.api import TTS

# # -----------------------------
# # Directories
# # -----------------------------
# VOICES_DIR = Path("voices")
# OUTPUT_DIR = Path("generated_audios")
# for d in (VOICES_DIR, OUTPUT_DIR):
#     d.mkdir(exist_ok=True)

# # -----------------------------
# # Language-specific models
# # -----------------------------
# LANGUAGE_MODELS = {
#     "en": "tts_models/multilingual/multi-dataset/vits",
#     "hi": "tts_models/hi/hindi/vits",
#     "mr": "tts_models/mr/marathi/vits",  # Check if available
# }

# # -----------------------------
# # GPU check
# # -----------------------------
# def _gpu_available() -> bool:
#     try:
#         if torch.cuda.is_available():
#             return True
#         if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
#             return True
#         return False
#     except Exception:
#         return False

# # -----------------------------
# # Load TTS model
# # -----------------------------
# @lru_cache(maxsize=3)
# def _get_tts(model_name: str = LANGUAGE_MODELS["en"]):
#     """
#     Lazy-load and cache TTS model for the given model_name.
#     """
#     use_gpu = _gpu_available()
#     device_str = "GPU/MPS" if use_gpu else "CPU"
#     print(f"[TTS] Loading model: {model_name} | Device={device_str}")
#     return TTS(model_name=model_name, progress_bar=False, gpu=use_gpu)

# # -----------------------------
# # Voice profiles
# # -----------------------------
# def list_saved_voices():
#     voices = ["Default (model voice)"]
#     for p in sorted(VOICES_DIR.glob("*.wav")):
#         voices.append(p.stem)
#     return voices

# def save_voice_profile(wav_path: str, profile_name: str) -> str:
#     safe = "".join(ch for ch in profile_name if ch.isalnum() or ch in ("_", "-")).strip("_-")
#     if not safe:
#         safe = f"profile_{uuid.uuid4().hex[:8]}"
#     dst = VOICES_DIR / f"{safe}.wav"
#     shutil.copy(wav_path, dst)
#     return str(dst)

# # -----------------------------
# # Language validation
# # -----------------------------
# def _get_valid_language(tts, requested_lang: str) -> str:
#     available_langs = getattr(tts, "languages", None)
#     if isinstance(available_langs, (list, dict)):
#         if requested_lang in available_langs or (isinstance(available_langs, dict) and requested_lang in available_langs.keys()):
#             return requested_lang
#         fallback = list(available_langs)[0]
#         print(f"[TTS] ⚠️ Requested language '{requested_lang}' not available. Using fallback: '{fallback}'")
#         return fallback
#     return requested_lang

# # -----------------------------
# # Generate TTS
# # -----------------------------
# def generate_tts(text: str, speaker_wav: str | None, file_name: str = "output.wav", language: str = "en") -> str:
#     out_path = OUTPUT_DIR / file_name
#     model_name = LANGUAGE_MODELS.get(language, LANGUAGE_MODELS["en"])
#     tts = _get_tts(model_name)

#     language = _get_valid_language(tts, language)

#     kwargs = dict(text=text, file_path=str(out_path), language=language)
#     if speaker_wav and os.path.exists(speaker_wav):
#         print(f"[TTS] Using speaker_wav: {speaker_wav}")
#         kwargs["speaker_wav"] = speaker_wav
#     elif speaker_wav:
#         print(f"[TTS] ⚠️ speaker_wav not found at {speaker_wav}; using default voice.")

#     tts.tts_to_file(**kwargs)
#     return str(out_path)

# # -----------------------------
# # Demo run
# # -----------------------------
# if __name__ == "__main__":
#     demo_text = "Hello! This is a quick test of the upgraded XTTS system."
#     print(generate_tts(demo_text, None, "demo.wav", language="en"))
