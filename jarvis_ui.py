import tkinter as tk
from tkinter import scrolledtext
import cv2
from PIL import Image, ImageTk

class JarvisUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Jarvis AI Interface")
        
        # Camera Feed Label
        self.video_label = tk.Label(window)
        self.video_label.pack()
        
        # Chat Section (Scrolled Text for conversation display)
        self.chat_display = scrolledtext.ScrolledText(window, width=60, height=10)
        self.chat_display.pack(pady=10)
        self.chat_display.config(state='disabled')  # Readonly initially
        
        # Input Entry for typing messages
        self.input_entry = tk.Entry(window, width=50)
        self.input_entry.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Send button
        self.send_button = tk.Button(window, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)
        
        # AI Learning Progress Label (just placeholder)
        self.learning_label = tk.Label(window, text="AI Learning Progress: Not started")
        self.learning_label.pack(pady=10)
        
        # Start camera capture
        self.cap = cv2.VideoCapture(0)
        self.update_frame()
    
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert image to RGB (OpenCV uses BGR)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.window.after(10, self.update_frame)  # update every 10ms
    
    def send_message(self):
        msg = self.input_entry.get()
        if msg.strip():
            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, f"You: {msg}\n")
            self.chat_display.config(state='disabled')
            self.input_entry.delete(0, tk.END)
            # TODO: Process msg with Jarvis AI and show response
            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, f"Jarvis: (Response will appear here)\n")
            self.chat_display.config(state='disabled')
            self.chat_display.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisUI(root)
    root.mainloop()
