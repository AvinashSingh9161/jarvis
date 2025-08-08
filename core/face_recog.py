import os, cv2, face_recognition
from config import FACES_DIR
os.makedirs(FACES_DIR, exist_ok=True)
_known_encodings = []
_known_names = []
def load_known_faces():
    global _known_encodings, _known_names
    _known_encodings = []
    _known_names = []
    for fname in os.listdir(FACES_DIR):
        if not fname.lower().endswith(('.png','.jpg','.jpeg')): continue
        path = os.path.join(FACES_DIR, fname)
        name = os.path.splitext(fname)[0]
        img = face_recognition.load_image_file(path)
        encs = face_recognition.face_encodings(img)
        if encs:
            _known_encodings.append(encs[0])
            _known_names.append(name)
def identify_face_from_frame(frame, tolerance=0.5):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)
    for enc in encodings:
        matches = face_recognition.compare_faces(_known_encodings, enc, tolerance=tolerance)
        if True in matches:
            idx = matches.index(True)
            return _known_names[idx]
    return None
def identify_from_webcam(timeout_seconds=3):
    cap = cv2.VideoCapture(0)
    import time
    start = time.time()
    name = None
    while time.time() - start < timeout_seconds:
        ret, frame = cap.read()
        if not ret: continue
        name = identify_face_from_frame(frame)
        if name: break
    cap.release()
    return name
# load on import
load_known_faces()
