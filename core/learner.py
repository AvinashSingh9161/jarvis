import json, os
from datetime import datetime
from config import LEARNED_FILE, DATA_DIR
os.makedirs(os.path.dirname(LEARNED_FILE), exist_ok=True)
def learn_command(command_text, intent='unknown', user_identity='unknown', lang='en'):
    entry = {'command': command_text, 'intent': intent, 'user': user_identity, 'lang': lang, 'timestamp': datetime.now().isoformat()}
    data = []
    if os.path.exists(LEARNED_FILE):
        try:
            with open(LEARNED_FILE,'r',encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            data = []
    data.append(entry)
    with open(LEARNED_FILE,'w',encoding='utf-8') as f:
        json.dump(data,f,indent=2,ensure_ascii=False)
