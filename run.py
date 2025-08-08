#!/usr/bin/env python3
"""Run script for Jarvis full project.
- Installs Python packages from requirements.txt if they are missing.
- Creates data folders.
- Attempts to start the assistant (core.main.run()).
"""
import os, sys, subprocess, time
from pathlib import Path

ROOT = Path(__file__).parent
REQ = ROOT / 'requirements.txt'
DATA_DIR = ROOT / 'jarvis_data'
LOG = DATA_DIR / 'jarvis_setup.log'

def ensure_data_dirs():
    DATA_DIR.mkdir(exist_ok=True)
    (DATA_DIR / 'faces').mkdir(exist_ok=True)
    (DATA_DIR / 'voices').mkdir(exist_ok=True)

def pip_install_requirements():
    print('Installing requirements (this may take several minutes)...')
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', str(REQ)])
        return True
    except subprocess.CalledProcessError as e:
        print('pip install failed:', e)
        print('You may need to install some packages manually (dlib/face-recognition).')
        return False

def start_assistant():
    try:
        from core.main import run
    except Exception as e:
        print('Import error:', e)
        return False
    run()
    return True

def main():
    ensure_data_dirs()
    # Try import a key package to detect if install needed
    try:
        import face_recognition  # noqa: F401
    except Exception:
        ok = pip_install_requirements()
        if not ok:
            print('\nSetup incomplete. Please check the errors and retry.')
            print('See README_WINDOWS.md for troubleshooting.')
            input('Press Enter to exit...')
            return
    # start
    started = start_assistant()
    if not started:
        print('Failed to start assistant. Check jarvis_data/jarvis.log for details.')
    else:
        print('Assistant finished.')

if __name__ == "__main__":
    main()
