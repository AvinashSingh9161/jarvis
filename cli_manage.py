import argparse, os
from core import face_recog, speaker_id
parser=argparse.ArgumentParser()
parser.add_argument('cmd',choices=['register_face','register_voice','list_users','delete_user'])
parser.add_argument('--name'); parser.add_argument('--file')
args=parser.parse_args()
if args.cmd=='register_face':
    if not args.name or not args.file: print('Provide --name and --file'); exit(1)
    face_recog_path=args.file; name=args.name
    # copy image
    dest=os.path.join('jarvis_data','faces',f"{name}.jpg")
    import shutil; shutil.copyfile(face_recog_path,dest)
    face_recog.load_known_faces(); print('Face registered:',name)
if args.cmd=='register_voice':
    if not args.name or not args.file: print('Provide --name and --file'); exit(1)
    speaker_id.register_voice(args.name,args.file); print('Voice registered:',args.name)
if args.cmd=='list_users':
    faces=[os.path.splitext(f)[0] for f in os.listdir('jarvis_data/faces') if f.lower().endswith(('.png','.jpg','.jpeg'))]
    voices=[os.path.splitext(f)[0] for f in os.listdir('jarvis_data/voices') if f.endswith('.npz')]
    users=sorted(set(faces+voices)); print('\n'.join(users))
if args.cmd=='delete_user':
    if not args.name: print('Provide --name'); exit(1)
    fpath=os.path.join('jarvis_data','faces',f"{args.name}.jpg"); vpath=os.path.join('jarvis_data','voices',f"{args.name}.npz")
    if os.path.exists(fpath): os.remove(fpath)
    if os.path.exists(vpath): os.remove(vpath)
    print('Deleted user assets')
