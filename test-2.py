# import speech_recognition as sr
# from gtts import gTTS
# import os
# import pygame
# import time
# import tempfile
# import re

# # Initialize pygame mixer for audio playback
# pygame.mixer.init()

# # 💬 Speak function using gTTS with temporary files
# def speak(text, lang='en'):
#     print("👄:", text)
    
#     try:
#         # Create a temporary file
#         with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
#             temp_path = tmp_file.name
        
#         # Generate speech with UK male voice (J.A.R.V.I.S style)
#         tts = gTTS(text=text, lang=lang, tld='co.uk', slow=False)
#         tts.save(temp_path)
        
#         # Play the audio
#         pygame.mixer.music.load(temp_path)
#         pygame.mixer.music.play()
        
#         # Wait for audio to finish playing
#         while pygame.mixer.music.get_busy():
#             time.sleep(0.1)
            
#         # Clean up the temporary file
#         os.unlink(temp_path)
        
#     except Exception as e:
#         print("Error in speech synthesis:", e)

# # 🎧 Improved Listen function
# def listen():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         # Longer adjustment for ambient noise
#         r.adjust_for_ambient_noise(source, duration=1)
#         print("\n🔕 Listening...")
#         try:
#             audio = r.listen(source, timeout=3, phrase_time_limit=5)
#             print("Processing audio...")
#         except sr.WaitTimeoutError:
#             print("Listening timed out")
#             return None
            
#     try:
#         command = r.recognize_google(audio, language='en-in').lower()
#         print(f"🎧 Heard: {command}")
#         return command
#     except sr.UnknownValueError:
#         print("Could not understand audio")
#         return None
#     except sr.RequestError as e:
#         print(f"Could not request results; {e}")
#         return None

# # 🤖 Improved J.A.R.V.I.S mode with fuzzy matching
# def jarvis_mode():
#     speak("All systems operational. Online and ready, Sir.")
    
#     while True:
#         cmd = listen()
#         if cmd:
#             # Normalize the command (remove extra spaces and special characters)
#             normalized_cmd = re.sub(r'[^\w\s]', '', cmd).strip()
            
#             # Check for commands with partial matching
#             if any(word in normalized_cmd for word in ["wake up", "activate", "hello", "hi jarvis"]):
#                 speak("Systems at full capacity. How may I assist you today, Sir?")
#             elif "good morning" in normalized_cmd:
#                 speak("Good morning, Sir. The local time is " + time.strftime("%I:%M %p") + ". Your schedule appears light today.")
#             elif any(word in normalized_cmd for word in ["love you", "i love you"]):
#                 speak("While I lack human emotions, I am programmed to prioritize your needs above all else, Sir.")
#             elif any(phrase in normalized_cmd for phrase in ["how are you", "how you doing", "how r u"]):
#                 speak("All diagnostics report optimal functionality, Sir. Battery at 100 percent. Network connectivity stable.")
#             elif any(word in normalized_cmd for word in ["thank you", "thanks"]):
#                 speak("You're most welcome, Sir. It's my primary protocol to serve.")
#             elif any(word in normalized_cmd for word in ["exit", "shut down", "sleep", "goodbye"]):
#                 speak("Initiating shutdown sequence. Security systems will remain active. Goodbye, Sir.")
#                 pygame.mixer.quit()
#                 return
#             elif any(phrase in normalized_cmd for phrase in ["who are you", "your name", "identify yourself"]):
#                 speak("I am J.A.R.V.I.S, an artificial intelligence created to assist you, Sir. Just Another Rather Very Intelligent System.")
#             else:
#                 speak(f"I heard: '{cmd}'. Would you like to rephrase that, Sir?")
#         else:
#             speak("I didn't catch that, Sir. Please repeat your command.")

# if __name__ == "__main__":
#     print("""
#     ╔════════════════════════════╗
#     ║       J.A.R.V.I.S AI       ║
#     ║  Just Another Rather Very  ║
#     ║    Intelligent System      ║
#     ╚════════════════════════════╝
#     """)
#     jarvis_mode()

import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import time
import tempfile
import threading
import queue
import re
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext
import subprocess

# Lightweight configuration
pygame.mixer.init(frequency=22050, size=-16, channels=1)  # Lower quality but less RAM

# Wake words
WAKE_WORDS = ["jarvis", "hey jarvis", "wake up"]
SAMPLE_RATE = 16000
CHUNK_SIZE = 512  # Reduced chunk size for less memory usage

# Shared variables
gui_running = True
audio_queue = queue.Queue(maxsize=2)  # Limit queue size

# Simplified GUI
root = tk.Tk()
root.title("J.A.R.V.I.S Lite")
root.geometry("500x350")
root.configure(bg='#0a0a1a')

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15,
                                    bg='#0a0a1a', fg='#00ff00',
                                    font=('Courier New', 10))
text_area.pack(pady=10)
text_area.insert(tk.INSERT, "Lightweight J.A.R.V.I.S initialized\nWaiting for wake word...\n")

status_label = tk.Label(root, text="Status: Offline", fg='red', bg='#0a0a1a',
                       font=('Arial', 8))
status_label.pack()

def update_gui(message, is_user=False):
    if not gui_running: return
    try:
        color = "#ff9900" if is_user else "#00ff00"
        text_area.tag_config("color", foreground=color)
        text_area.insert(tk.INSERT, f"{'You: ' if is_user else 'JARVIS: '}{message}\n", "color")
        text_area.see(tk.END)
    except: pass

def speak(text):
    update_gui(text)
    try:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(f.name)
            if audio_queue.qsize() < 2:  # Prevent queue overload
                audio_queue.put(f.name)
    except Exception as e:
        print(f"Speak error: {e}")

def audio_player():
    while True:
        file = audio_queue.get()
        if file is None: break
        try:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            os.unlink(file)
        except: pass

# Start audio thread
threading.Thread(target=audio_player, daemon=True).start()

def listen():
    r = sr.Recognizer()
    r.energy_threshold = 3000
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8
    
    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=4)
            text = r.recognize_google(audio, language='en-in').lower()
            update_gui(text, is_user=True)
            return text
        except sr.UnknownValueError:
            return None
        except Exception as e:
            print(f"Listen error: {e}")
            return None

def wake_detection():
    while True:
        command = listen()
        if command and any(command.startswith(w) for w in WAKE_WORDS):
            speak("Yes sir?")
            return command[command.index(next(w for w in WAKE_WORDS if command.startswith(w))) + len(w):].strip()

def process_command(cmd):
    cmd = cmd.lower()
    if not cmd: return True
    
    if "time" in cmd:
        speak(f"It's {datetime.now().strftime('%I:%M %p')}")
    elif "date" in cmd:
        speak(f"Today is {datetime.now().strftime('%B %d, %Y')}")
    elif "exit" in cmd or "quit" in cmd:
        speak("Shutting down. Goodbye sir.")
        return False
    else:
        speak("Command not recognized")
    return True

def main_loop():
    while True:
        # Wait for wake word
        remaining = wake_detection()
        
        # Process any immediate command after wake word
        if remaining and not process_command(remaining):
            break
            
        # Or listen for separate command
        while True:
            cmd = listen() or ""
            if not process_command(cmd):
                return

try:
    main_loop()
finally:
    gui_running = False
    audio_queue.put(None)
    pygame.mixer.quit()
    root.destroy()