import os, numpy as np, librosa
from sklearn.neighbors import KNeighborsClassifier
from joblib import dump, load
import sounddevice as sd, soundfile as sf
from config import VOICES_DIR, DATA_DIR
os.makedirs(VOICES_DIR, exist_ok=True)
MODEL_PATH = os.path.join(DATA_DIR, 'speaker_model.joblib')
def extract_features(audio_path, sr=16000, n_mfcc=20):
    y, _ = librosa.load(audio_path, sr=sr)
    y, _ = librosa.effects.trim(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    features = np.concatenate((mfcc.mean(axis=1), mfcc.std(axis=1)))
    return features
def register_voice(username, audio_path):
    features = extract_features(audio_path)
    np.savez(os.path.join(VOICES_DIR, f"{username}.npz"), features=features)
    train_model()
    return True
def load_registry():
    X = []
    y = []
    for fname in os.listdir(VOICES_DIR):
        if not fname.endswith('.npz'): continue
        data = np.load(os.path.join(VOICES_DIR, fname))
        feat = data['features']
        name = os.path.splitext(fname)[0]
        X.append(feat); y.append(name)
    if X: X = np.vstack(X)
    else: X = None
    return X, y
def train_model():
    X, y = load_registry()
    if X is None:
        if os.path.exists(MODEL_PATH): os.remove(MODEL_PATH)
        return
    clf = KNeighborsClassifier(n_neighbors=min(3, len(y)))
    clf.fit(X, y)
    dump(clf, MODEL_PATH)
def identify_speaker(audio_path):
    if not os.path.exists(MODEL_PATH): return None
    clf = load(MODEL_PATH)
    feat = extract_features(audio_path)
    pred = clf.predict([feat])
    return pred[0]
def record_sample(dst_path, duration=3, sr=16000):
    print('Recording sample...') 
    rec = sd.rec(int(duration * sr), samplerate=sr, channels=1)
    sd.wait()
    sf.write(dst_path, rec, sr)
    return dst_path
