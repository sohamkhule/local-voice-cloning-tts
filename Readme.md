# 🎙 Local Voice-Cloning TTS


A **local text-to-speech (TTS) application** using **Coqui TTS** with zero-shot voice cloning.  
Built with **Streamlit**, this app allows users to record or upload their voice, save it as a profile, and generate speech in multiple languages.

---

## 🔹 Features

- Record voice using a microphone or upload a WAV file (8–15 seconds)
- Save multiple voice profiles for future TTS generation
- Generate TTS from text using a selected cloned voice
- Choose output language for TTS
- View previously generated audios with a dropdown
- Delete individual generated audios
- Download generated audios

---

## 🔹 Project Structure

local-voice-cloning-tts/
│
├─ uploads/ # Uploaded voice samples (auto-generated)
├─ voices/ # Saved voice profiles (auto-generated)
├─ generated_audios/ # Generated TTS files (auto-generated)
├─ tts_engine.py # TTS helper functions
├─ app.py # Main Streamlit application
├─ requirements.txt # Python dependencies
├─ README.md # Project documentation 

 Note: Folders `uploads/`, `voices/`, and `generated_audios/` are auto-created by the app and should not be manually modified.

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
