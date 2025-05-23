# Program Artificial Runner Assistant (ARA)         menggunakan bahasa python dengan tujuan meneyelesaikan proyek akhir mata kuliah Dasar Komputer 
# anggota kelompok; Raditya Pradipa Ivantoro (2409460), dan Raditya Putra Nafisa (2409461)

# Section Modules Installation
import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import webbrowser
import subprocess
import pyttsx3
from datetime import datetime
import threading
import time
import os
import sys 

# Section GUI Window Building
class PersonalAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ARA - Personal Assistant")
        self.root.geometry("500x500")
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()

        self.build_gui()
        self.greet()

    def build_gui(self):
        self.root.configure(bg="#1e1e1e")  

        self.chat_display = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            state='disabled',
            font=("Consolas", 10),
            bg="#292929",  
            fg="#dcdcdc",  
            insertbackground="white"
        )
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.entry = tk.Entry(self.root, font=("Helvetica", 12), bg="#3c3f41", fg="white", insertbackground="white")
        self.entry.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.entry.bind("<Return>", lambda event: self.process_text_command())
        
        button_frame = tk.Frame(self.root, bg="#1e1e1e")
        button_frame.pack()

        self.send_button = tk.Button(
            button_frame,
            text="Send",
            command=self.process_text_command,
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            padx=10,
            pady=5
        )
        self.send_button.pack(side=tk.LEFT, padx=5)

        
        self.voice_button = tk.Button(
            button_frame,
            text="Voice Command",
            command=self.listen_thread,
            bg="#2196F3",
            fg="white",
            activebackground="#1976D2",
            padx=10,
            pady=5
        )
        self.voice_button.pack(side=tk.LEFT, padx=5)

# Section Voice System

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def greet(self):
        hour = datetime.now().hour
        if 5 <= hour < 10:
            greeting = "Good Morning! with ARA, Welcome back operator"
        elif 10 <= hour < 15:
            greeting = "Good Afternoon! with ARA, Welcome back operator"
        elif 15 <= hour < 19:
            greeting = "Good Evening! with ARA, Welcome back operator"
        else:
            greeting = "Good Night! with ARA, Welcome back operator"

        self.display_message("ARA", greeting)
        self.speak(greeting)

# Section Display Message

    def display_message(self, sender, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

# Section Voice Command Processing

    def recognize_speech(self):
        with sr.Microphone() as source:
            self.display_message("ARA", "Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio, language="id-ID").lower()
                self.display_message("OPERATOR (via voice)", command)
                self.execute_command(command)
            except sr.UnknownValueError:
                self.display_message("ARA", "Sorry, I didn't understand.")
                self.speak("Sorry, I didn't understand.")
            except sr.RequestError:
                self.display_message("ARA", "Technical issue encountered.")
                self.speak("Technical issue encountered.")
            except sr.WaitTimeoutError:
                self.display_message("ARA", "No command detected.")
                self.speak("No command detected.")

# Section Threading for Voice Command

    def listen_thread(self):
        threading.Thread(target=self.recognize_speech).start()

# Section Text Command Processing
    def process_text_command(self):
        command = self.entry.get().lower()
        self.entry.delete(0, tk.END)
        if command.strip():
            self.display_message("OPERATOR", command)
            self.execute_command(command)

# Section Commands list (Manual)
    def execute_command(self, command):
        if not command:
            return

        if "hello" in command:
            response = "Hello Operator, what can I do for you?"
        elif "open youtube" in command:
            response = "Open YouTube"
            webbrowser.open("https://www.youtube.com")
        elif "open whatsapp" in command:
            response = "Open WhatsApp"
            webbrowser.open(("whatsapp.exe"), shell=True)
        elif "open google" in command:
            response = "Open Google"
            webbrowser.open("https://www.google.com")
        elif "open notepad" in command:
            response = "Open Notepad"
            subprocess.Popen(["notepad.exe"])
        elif "open kalkulator" in command:
            response = "Open Kalkulator"
            subprocess.Popen("calc.exe")
        elif "open f-35" in command:
            response = "Open F35 manual"
            subprocess.Popen(r"D:\Classified Doc\Lockheed Martin F35 Manual.pdf", shell=True)
        elif "open ucav" in command:
            response = "Open UCAV Predator Manual"
            subprocess.Popen(r"D:\Classified Doc\General Atomics MQ-1 Predator Manual.pdf", shell=True)
        elif "what time is it" in command:
            current_time = datetime.now().strftime("%H:%M")
            response = f"Current time is {current_time}"
        elif "what day is it now" in command:
            current_date = datetime.now().strftime("%d %B %Y")
            response = f"Today is {current_date}"
        elif "thank you" in command:
            response = "You're welcome"
            subprocess.Popen(("TLauncher.exe"), shell=True)
        elif "system out" in command or "berhenti" in command:
            response = "System out, see you next time."
            self.display_message("ARA", response)
            self.speak(response)
            self.root.quit()
            return
        else:
            response = "Sorry, command invalid. Can you repeat it?"

        self.display_message("ARA", response)
        self.speak(response)

# Section Main Function
if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalAssistantGUI(root)
    root.mainloop()
