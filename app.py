import uuid
from pathlib import Path
import streamlit as st

# Mic recorder import (optional)
_MIC_OK = True
try:
    from st_mic_recorder import mic_recorder
except Exception:
    _MIC_OK = False

from tts_engine import generate_tts, list_saved_voices, save_voice_profile, _get_tts

# Directories
UPLOAD_DIR = Path("uploads")
VOICES_DIR = Path("voices")
OUTPUT_DIR = Path("generated_audios")
for d in (UPLOAD_DIR, VOICES_DIR, OUTPUT_DIR):
    d.mkdir(exist_ok=True)

st.set_page_config(page_title="Local Voice-Cloning TTS", page_icon="🎙", layout="centered")
st.title("🎙 Local Voice-Cloning TTS")

with st.expander("Status / Tips", expanded=False):
    st.markdown(
        "- **Model**: Coqui TTS (`xtts_v1`) for multilingual zero-shot cloning.\n"
        "- Voice profiles are stored in the `voices/` folder.\n"
        "- Use microphone if available; otherwise upload a short WAV (8–15 sec).\n"
    )

# ---------------------------
# 1) Capture a new voice sample
# ---------------------------
st.header("1) Capture your voice sample (1–2 sentences)")
recorded_bytes = None

if _MIC_OK:
    audio = mic_recorder(
        start_prompt="🎙 Start Recording",
        stop_prompt="⏹ Stop",
        just_once=True,
        use_container_width=True
    )
    if audio and "bytes" in audio:
        recorded_bytes = audio["bytes"]
else:
    st.info("Mic component not available. Use the uploader below.")
    up = st.file_uploader("Upload WAV (8–15 seconds)", type=["wav"])
    if up:
        recorded_bytes = up.read()

if recorded_bytes:
    sample_path = UPLOAD_DIR / f"{uuid.uuid4().hex}.wav"
    sample_path.write_bytes(recorded_bytes)
    st.success(f"Sample saved: `{sample_path.name}`")
    st.audio(str(sample_path))

    with st.form("save_profile_form", clear_on_submit=True):
        profile_name = st.text_input("Profile name (e.g., soham_1)", max_chars=40)
        save_btn = st.form_submit_button("💾 Save voice profile")
        if save_btn:
            if not profile_name.strip():
                st.error("Please enter a profile name.")
            else:
                saved_as = save_voice_profile(str(sample_path), profile_name.strip())
                st.success(f"Saved profile: `{saved_as}`")
                st.rerun()  # ✅ Updated from deprecated experimental_rerun

# ---------------------------
# 2) Choose a voice
# ---------------------------
st.header("2) Choose a voice")
voices = list_saved_voices()
voice_choice = st.selectbox("Voice profile", voices, index=0)

# ---------------------------
# 3) Text to synthesize
# ---------------------------
st.header("3) Text to synthesize")
text = st.text_area(
    "Enter text",
    value="Hello! This is a test in my cloned voice.",
    height=120
)

# ---------------------------
# ---------------------------
# 4) Generate speech
# ---------------------------
st.header("4) Generate")

# ✅ Get available languages dynamically from TTS model
tts_instance = _get_tts()
available_langs = getattr(tts_instance, "languages", ["en"])
if isinstance(available_langs, dict):
    available_langs = list(available_langs.keys())

language = st.selectbox(
    "Select language",
    available_langs,
    index=0,
    help="Choose the output language for the TTS."
)

col_a, col_b = st.columns([1, 2])
with col_a:
    gen = st.button("🟢 Generate Speech", use_container_width=True)

if gen:
    if not text.strip():
        st.error("Please enter some text.")
    else:
        st.info("Generating audio… first run may take longer while the model loads.")
        speaker_wav = None
        if voice_choice != "Default (model voice)":
            candidate = VOICES_DIR / f"{voice_choice}.wav"
            if candidate.exists():
                speaker_wav = str(candidate)
            else:
                st.warning(f"Selected profile `{voice_choice}` not found on disk; using default voice.")

        out_name = f"{uuid.uuid4().hex}.wav"
        try:
            out_path = generate_tts(
                text=text,
                speaker_wav=speaker_wav,
                file_name=out_name,
                language=language
            )
            st.success(f"Done! Saved: `{out_path}`")
            st.audio(out_path)
            st.markdown(f"[⬇️ Download audio]({out_path})")
        except Exception as e:
            st.error(f"Generation failed: {e}")  

# ---------------------------
# ---------------------------
# 5) Show previously generated audios with delete option
# ---------------------------
st.header("🎧 Previously Generated Audios")
generated_files = sorted(OUTPUT_DIR.glob("*.wav"), key=lambda x: x.stat().st_mtime, reverse=True)

if generated_files:
    for f in generated_files:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{f.name}**")
            st.audio(str(f))
        with col2:
            if st.button("🗑 Delete", key=f.name):
                try:
                    f.unlink()  # delete the file
                    st.success(f"Deleted `{f.name}`")
                    st.rerun()  # refresh the page to update the list
                except Exception as e:
                    st.error(f"Failed to delete `{f.name}`: {e}")
else:
    st.info("No generated audios yet.")







# import uuid
# from pathlib import Path
# import streamlit as st

# # Mic recorder import (optional)
# _MIC_OK = True
# try:
#     from st_mic_recorder import mic_recorder
# except Exception:
#     _MIC_OK = False

# from tts_engine import generate_tts, list_saved_voices, save_voice_profile, _get_tts, LANGUAGE_MODELS

# # -----------------------------
# # Directories
# # -----------------------------
# UPLOAD_DIR = Path("uploads")
# VOICES_DIR = Path("voices")
# OUTPUT_DIR = Path("generated_audios")
# for d in (UPLOAD_DIR, VOICES_DIR, OUTPUT_DIR):
#     d.mkdir(exist_ok=True)

# # -----------------------------
# # Streamlit config
# # -----------------------------
# st.set_page_config(page_title="Local Voice-Cloning TTS", page_icon="🎙", layout="centered")
# st.title("🎙 Local Voice-Cloning TTS")

# with st.expander("Status / Tips", expanded=False):
#     st.markdown(
#         "- **Model**: Coqui TTS (`vits`) for multilingual zero-shot cloning.\n"
#         "- Voice profiles are stored in the `voices/` folder.\n"
#         "- Use microphone if available; otherwise upload a short WAV (8–15 sec).\n"
#     )

# # ---------------------------
# # 1) Capture a new voice sample
# # ---------------------------
# st.header("1) Capture your voice sample (1–2 sentences)")
# recorded_bytes = None

# if _MIC_OK:
#     audio = mic_recorder(
#         start_prompt="🎙 Start Recording",
#         stop_prompt="⏹ Stop",
#         just_once=True,
#         use_container_width=True
#     )
#     if audio and "bytes" in audio:
#         recorded_bytes = audio["bytes"]
# else:
#     st.info("Mic component not available. Use the uploader below.")
#     up = st.file_uploader("Upload WAV (8–15 seconds)", type=["wav"])
#     if up:
#         recorded_bytes = up.read()

# if recorded_bytes:
#     sample_path = UPLOAD_DIR / f"{uuid.uuid4().hex}.wav"
#     sample_path.write_bytes(recorded_bytes)
#     st.success(f"Sample saved: `{sample_path.name}`")
#     st.audio(str(sample_path))

#     with st.form("save_profile_form", clear_on_submit=True):
#         profile_name = st.text_input("Profile name (e.g., soham_1)", max_chars=40)
#         save_btn = st.form_submit_button("💾 Save voice profile")
#         if save_btn:
#             if not profile_name.strip():
#                 st.error("Please enter a profile name.")
#             else:
#                 saved_as = save_voice_profile(str(sample_path), profile_name.strip())
#                 st.success(f"Saved profile: `{saved_as}`")
#                 st.experimental_rerun()

# # ---------------------------
# # 2) Choose a voice
# # ---------------------------
# st.header("2) Choose a voice")
# voices = list_saved_voices()
# voice_choice = st.selectbox("Voice profile", voices, index=0)

# # ---------------------------
# # 3) Text to synthesize
# # ---------------------------
# st.header("3) Text to synthesize")
# text = st.text_area(
#     "Enter text",
#     value="Hello! This is a test in my cloned voice.",
#     height=120
# )

# # ---------------------------
# # 4) Generate speech
# # ---------------------------
# st.header("4) Generate")

# # ---------------------------
# # Language selection
# # ---------------------------
# language = st.selectbox(
#     "Select language",
#     options=list(LANGUAGE_MODELS.keys()),
#     index=0,
#     help="Choose the output language for the TTS."
# )

# col_a, col_b = st.columns([1, 2])
# with col_a:
#     gen = st.button("🟢 Generate Speech", use_container_width=True)

# if gen:
#     if not text.strip():
#         st.error("Please enter some text.")
#     else:
#         st.info("Generating audio… first run may take longer while the model loads.")

#         # Load the correct model for the selected language
#         model_name = LANGUAGE_MODELS.get(language, LANGUAGE_MODELS["en"])
#         tts_instance = _get_tts(model_name)

#         speaker_wav = None
#         if voice_choice != "Default (model voice)":
#             candidate = VOICES_DIR / f"{voice_choice}.wav"
#             if candidate.exists():
#                 speaker_wav = str(candidate)
#             else:
#                 st.warning(f"Selected profile `{voice_choice}` not found; using default voice.")

#         out_name = f"{uuid.uuid4().hex}.wav"
#         try:
#             out_path = generate_tts(
#                 text=text,
#                 speaker_wav=speaker_wav,
#                 file_name=out_name,
#                 language=language
#             )
#             st.success(f"Done! Saved: `{out_path}`")
#             st.audio(out_path)
#             st.markdown(f"[⬇️ Download audio]({out_path})")
#         except Exception as e:
#             st.error(f"Generation failed: {e}")

