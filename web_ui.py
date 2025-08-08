from flask import Flask, request, jsonify
import os
from core import face_recog, speaker_id
app=Flask(__name__)
@app.route('/users',methods=['GET'])
def users():
    faces=[os.path.splitext(f)[0] for f in os.listdir('jarvis_data/faces') if f.lower().endswith(('.png','.jpg','.jpeg'))]
    voices=[os.path.splitext(f)[0] for f in os.listdir('jarvis_data/voices') if f.endswith('.npz')]
    return jsonify({'users':sorted(list(set(faces+voices)))})
@app.route('/register/face',methods=['POST'])
def reg_face():
    name=request.form.get('name'); file=request.files.get('file')
    if not name or not file: return 'name and file required',400
    path=os.path.join('jarvis_data','faces',f"{name}.jpg"); file.save(path); face_recog.load_known_faces(); return 'ok'
@app.route('/register/voice',methods=['POST'])
def reg_voice():
    name=request.form.get('name'); file=request.files.get('file')
    if not name or not file: return 'name and file required',400
    path=os.path.join('jarvis_data','voices',f"{name}.wav"); file.save(path)
    speaker_id.register_voice(name,path); return 'ok'
if __name__=='__main__': app.run(port=5002)
