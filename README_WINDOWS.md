Jarvis — Full offline-capable assistant (English + Hindi)
========================================================

Quick start (Windows):
1. Extract this ZIP to a folder, e.g. C:\Users\Avinash\Jarvis
2. Open PowerShell or CMD in that folder.
3. Run: python run.py
   - On first run the script will attempt to install required Python packages.
   - If installation fails for dlib/face-recognition, follow the 'Troubleshooting' section below.
4. After setup finishes, run will start the assistant. Speak in English or Hindi.
5. To stop, say or type 'exit' or 'band'.

Troubleshooting (common issues):
- face_recognition requires dlib. If pip install fails, install Visual Studio Build Tools
  (Desktop development with C++) then install a prebuilt wheel for dlib matching your Python version.
- If PyAudio fails to install, use pipwin: 'pip install pipwin' then 'pipwin install pyaudio'.
- If VOSK models are not downloaded automatically, download manually from https://alphacephei.com/vosk/models/ and unzip into project root.
- All runtime data is stored under 'jarvis_data/' so you can move the project folder without breaking paths.

If you hit any errors, copy the terminal traceback and the file jarvis_data/jarvis.log and share it with me — I'll debug it step-by-step.
