# Config - keeps all data inside DATA_DIR so project is portable
DATA_DIR = "jarvis_data"
FACES_DIR = f"{DATA_DIR}/faces"
VOICES_DIR = f"{DATA_DIR}/voices"
WEB_CACHE_FILE = f"{DATA_DIR}/web_cache.json"
LEARNED_FILE = f"{DATA_DIR}/learned_commands.json"
LOG_FILE = f"{DATA_DIR}/jarvis.log"

# Behavior toggles
ALLOW_WEB_ENRICH = False  # set True to enable web enrichment (requires internet)
SUPPORTED_LANGUAGES = ["en", "hi"]  # en = English, hi = Hindi

# VOSK model folders expected (optional auto-download may be attempted)
VOSK_MODELS = {
    "en": "vosk-model-small-en-us-0.15",
    "hi": "vosk-model-small-hi-0.22"
}

# Security
ALLOWED_USERS = ["admin"]
