import pyttsx3
_engine = None
def _get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
    return _engine
def speak(text):
    if not text:
        return
    eng = _get_engine()
    eng.say(text)
    eng.runAndWait()
