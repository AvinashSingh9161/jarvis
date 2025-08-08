import os, wave, json, tempfile
from pathlib import Path
from config import VOSK_MODELS, SUPPORTED_LANGUAGES
try:
    from vosk import Model, KaldiRecognizer
    VOSK_AVAILABLE = True
except Exception:
    VOSK_AVAILABLE = False
# fallback to SpeechRecognition google if VOSK not present
def transcribe_file_auto(wav_path):
    """Try to transcribe using VOSK English/Hindi models if present; else fallback to SpeechRecognition."""
    # If VOSK available, try models
    if VOSK_AVAILABLE:
        from vosk import Model, KaldiRecognizer
        best_text = ''
        best_lang = None
        for lang, model_folder in VOSK_MODELS.items():
            if os.path.exists(model_folder):
                try:
                    wf = wave.open(wav_path, 'rb')
                    rec = KaldiRecognizer(Model(model_folder), wf.getframerate())
                    text = ''
                    while True:
                        data = wf.readframes(4000)
                        if len(data) == 0:
                            break
                        if rec.AcceptWaveform(data):
                            res = json.loads(rec.Result())
                            text += ' ' + res.get('text','')
                    text += ' ' + json.loads(rec.FinalResult()).get('text','')
                    text = text.strip()
                    if len(text.split()) > len(best_text.split()):
                        best_text = text
                        best_lang = lang
                except Exception:
                    continue
        if best_text:
            return best_text, best_lang or SUPPORTED_LANGUAGES[0]
    # Fallback using SpeechRecognition (requires internet)
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio = r.record(source)
        # try english then hindi
        try:
            txt = r.recognize_google(audio, language='en-IN')
            if txt:
                return txt, 'en'
        except Exception:
            pass
        try:
            txt = r.recognize_google(audio, language='hi-IN')
            if txt:
                return txt, 'hi'
        except Exception:
            pass
    except Exception:
        pass
    return '', None

def transcribe_file_from_mic(duration=3, out_wav=None):
    import sounddevice as sd, soundfile as sf
    fs = 16000
    if out_wav is None:
        out_wav = os.path.join('jarvis_data', 'tmp_mic.wav')
    print('Recording audio...')
    rec = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    sf.write(out_wav, rec, fs)
    return transcribe_file_auto(out_wav)
