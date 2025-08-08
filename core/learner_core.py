import os, json
from datetime import datetime
from config import LEARNED_FILE, WEB_CACHE_FILE, ALLOW_WEB_ENRICH
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
try:
    with open(LEARNED_FILE,'r',encoding='utf-8') as f:
        learned_data = json.load(f)
except Exception:
    learned_data = []
try:
    with open(WEB_CACHE_FILE,'r',encoding='utf-8') as f:
        web_cache = json.load(f)
except Exception:
    web_cache = {}
def save_learned():
    with open(LEARNED_FILE,'w',encoding='utf-8') as f:
        json.dump(learned_data,f,indent=2,ensure_ascii=False)
def save_cache():
    with open(WEB_CACHE_FILE,'w',encoding='utf-8') as f:
        json.dump(web_cache,f,indent=2,ensure_ascii=False)
def synthetic_augment(text):
    variants = [text, text+' please', 'please '+text]
    return ' || '.join(variants)
_vectorizer=None; _tf=None; _texts=[]; _keys=[]
def build_index():
    global _vectorizer,_tf,_texts,_keys
    texts=[]; keys=[]
    for i,e in enumerate(learned_data):
        texts.append(e.get('command','')); keys.append(('learned',i))
    for q,d in web_cache.items():
        for s in d.get('snippets',[]): texts.append(s.get('snippet','') or s.get('title','')); keys.append(('web',q))
    for e in learned_data: texts.append(synthetic_augment(e.get('command',''))); keys.append(('synth',e.get('command','')))
    if not texts: _texts=[]; _keys=[]; _tf=None; return
    _vectorizer=TfidfVectorizer(stop_words='english',max_features=5000)
    _tf=_vectorizer.fit_transform(texts); _texts=texts; _keys=keys
def match(text, top_k=3):
    if _tf is None: build_index(); 
    if _tf is None: return []
    q=_vectorizer.transform([text])
    sims=cosine_similarity(q,_tf).flatten()
    idx=np.argsort(-sims)[:top_k]; res=[]
    for i in idx: res.append({'key':_keys[i],'text':_texts[i],'score':float(sims[i])})
    return res
def guess_intent(text):
    t=text.lower()
    if 'time' in t or 'kya time' in t: return 'get_time',0.99
    if 'remind' in t or 'reminder' in t: return 'set_reminder',0.98
    if 'open' in t or 'khol' in t: return 'open_website',0.97
    m=match(text,top_k=3)
    if m and m[0]['score']>0.35:
        key=m[0]['key']
        if key[0]=='learned':
            intent=learned_data[key[1]].get('intent','small_talk')
            return intent,m[0]['score']
    return 'small_talk',0.3
