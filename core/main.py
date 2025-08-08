import time
import os
from config import DATA_DIR, FACES_DIR, VOICES_DIR, ALLOWED_USERS, SUPPORTED_LANGUAGES
from .stt import transcribe_file_from_mic, transcribe_file_auto
from .tts import speak
from .face_recog import identify_from_webcam, load_known_faces
from .speaker_id import record_sample, identify_speaker, register_voice
from .learner import learn_command
from ui import JarvisUI
import threading

# Load known faces at start
load_known_faces()

def jarvis_loop(app):
    app.update_progress(0, "Jarvis starting...")

    speak('Jarvis online. How can I assist you?')

    try:
        progress = 0
        while True:
            # Update some progress indicator for demonstration
            progress = (progress + 1) % 101
            app.update_progress(progress, f"Running... {progress}%")

            # Record 3s sample for speaker id and STT
            tmp = os.path.join(DATA_DIR, 'tmp_latest.wav')
            record_sample(tmp, duration=3)

            # Identify speaker & face
            user = identify_speaker(tmp) or 'unknown'
            face_user = identify_from_webcam(timeout_seconds=2)
            if face_user:
                user = face_user

            print('User:', user)

            # Transcribe audio
            text, lang = transcribe_file_auto(tmp)

            if not text:
                print('No speech detected. Try again.')
                app.update_progress(progress, "No speech detected. Waiting...")
                time.sleep(1)
                continue

            print(f'Heard ({lang}):', text)

            # Learn command
            learn_command(text, intent='unknown', user_identity=user, lang=lang)

            # Respond to commands
            if any(w in text.lower() for w in ['exit', 'band']):
                speak('Shutting down. Goodbye.')
                app.update_progress(100, "Shutting down...")
                break

            if 'time' in text.lower() or 'kya time' in text.lower():
                from datetime import datetime
                now = datetime.now().strftime('%I:%M %p')
                speak(f'Current time is {now}')
            else:
                speak('I heard: ' + text)

            time.sleep(0.5)

    except KeyboardInterrupt:
        print('Interrupted by user. Exiting...')
        app.update_progress(0, "Interrupted. Exiting...")

def run():
    app = JarvisUI()

    # Run jarvis_loop in a separate thread to keep UI responsive
    jarvis_thread = threading.Thread(target=jarvis_loop, args=(app,), daemon=True)
    jarvis_thread.start()

    app.run()
