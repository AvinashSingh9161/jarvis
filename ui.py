import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import cv2
from PIL import Image, ImageTk

class JarvisUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jarvis AI Assistant")
        self.root.geometry("900x600")

        # Camera feed frame
        self.camera_frame = ttk.LabelFrame(self.root, text="Camera Feed")
        self.camera_frame.place(x=10, y=10, width=560, height=420)

        self.lmain = tk.Label(self.camera_frame)
        self.lmain.pack()

        # Chat frame
        self.chat_frame = ttk.LabelFrame(self.root, text="Chat")
        self.chat_frame.place(x=580, y=10, width=300, height=420)

        self.chat_log = scrolledtext.ScrolledText(self.chat_frame, state='disabled', wrap=tk.WORD)
        self.chat_log.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.chat_entry = ttk.Entry(self.chat_frame)
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.chat_entry.bind("<Return>", self.send_message)

        self.send_button = ttk.Button(self.chat_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # AI Learning Progress frame
        self.progress_frame = ttk.LabelFrame(self.root, text="AI Learning Progress")
        self.progress_frame.place(x=10, y=440, width=870, height=140)

        self.progress_label = ttk.Label(self.progress_frame, text="Training not started")
        self.progress_label.pack(pady=10)

        self.progress_bar = ttk.Progressbar(self.progress_frame, orient='horizontal', length=800, mode='determinate')
        self.progress_bar.pack(pady=5)

        self.training_started = False

        # Start camera in a thread so UI doesn't freeze
        self.cap = cv2.VideoCapture(0)
        self.camera_thread = threading.Thread(target=self.show_camera)
        self.camera_thread.daemon = True
        self.camera_thread.start()

    def show_camera(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                # Convert to RGB
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.lmain.imgtk = imgtk
                self.lmain.configure(image=imgtk)
            else:
                self.lmain.configure(text="No Camera Found")
            # Refresh frame every 30 ms
            self.lmain.after(30)

    def send_message(self, event=None):
        msg = self.chat_entry.get().strip()
        if msg:
            self.chat_log.config(state='normal')
            self.chat_log.insert(tk.END, f"You: {msg}\n")
            self.chat_log.config(state='disabled')
            self.chat_log.yview(tk.END)
            self.chat_entry.delete(0, tk.END)
            # Yahan tum AI response generate karne ka code daal sakte ho
            self.respond_to_message(msg)

    def respond_to_message(self, msg):
        # Dummy response example
        response = f"Jarvis: You said '{msg}'"
        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, response + "\n")
        self.chat_log.config(state='disabled')
        self.chat_log.yview(tk.END)

    def update_progress(self, percent, status_text):
        self.progress_bar['value'] = percent
        self.progress_label.config(text=status_text)
        self.root.update_idletasks()

    def run(self):
        self.root.mainloop()

    def close(self):
        self.cap.release()
        self.root.destroy()
