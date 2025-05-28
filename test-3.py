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
import pywhatkit
import tkinter as tk
from tkinter import scrolledtext
import random
import subprocess

# Lightweight configuration
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)  # Reduced audio quality for less RAM usage

# Wake words
WAKE_WORDS = ["jarvis", "hey jarvis", "wake up"] 
SAMPLE_RATE = 16000
CHUNK_SIZE = 512  # Reduced chunk size for less memory usage

# Global flags
gui_running = True
audio_queue = queue.Queue()

# Create GUI
root = tk.Tk()
root.title("J.A.R.V.I.S AI System")
root.geometry("500x350")
root.configure(bg='#0a0a1a')

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20,
                                    bg='#0a0a1a', fg='#00ff00',
                                    font=('Courier New', 12))
text_area.pack(pady=20)
text_area.insert(tk.INSERT, "System initialized. Waiting for wake word...\n")
text_area.see(tk.END)

status_label = tk.Label(root, text="Status: Offline", fg='red', bg='#0a0a1a',
                       font=('Arial', 10, 'bold'))
status_label.pack()

def update_gui(message, is_user=False):
    global gui_running
    if not gui_running:
        return
        
    try:
        tag = "user" if is_user else "jarvis"
        color = "#ff9900" if is_user else "#00ff00"
        text_area.tag_config(tag, foreground=color)
        text_area.insert(tk.INSERT, f"{'👤 You' if is_user else '🤖 J.A.R.V.I.S'}: {message}\n", tag)
        text_area.see(tk.END)
        root.update()
    except tk.TclError:
        pass

def speak(text, lang='en', emotion='neutral'):
    update_gui(text)
    
    def _speak():
        try:
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
                temp_path = tmp_file.name
            
            tts = gTTS(text=text, lang=lang, tld='co.uk', slow=(emotion == 'serious'))
            tts.save(temp_path)
            audio_queue.put(temp_path)
            
        except Exception as e:
            print("Speech error:", e)
    
    threading.Thread(target=_speak).start()

def audio_player():
    while True:
        audio_file = audio_queue.get()
        if audio_file is None:
            break
            
        try:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
        finally:
            pygame.mixer.music.stop()
            try:
                os.unlink(audio_file)
            except:
                pass

player_thread = threading.Thread(target=audio_player)
player_thread.daemon = True
player_thread.start()

def listen(timeout=3, phrase_time_limit=5):
    r = sr.Recognizer()
    r.energy_threshold = 3000
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.5
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        status_label.config(text="Status: Listening", fg='yellow')
        
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            status_label.config(text="Status: Processing", fg='orange')
            
            command = r.recognize_google(audio, language='en-in').lower()
            update_gui(command, is_user=True)
            return command
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None
def get_time():
    return datetime.now().strftime("%I:%M %p")

def get_date():
    return datetime.now().strftime("%A, %B %d, %Y")

# 🎵 Media functions
def play_on_youtube(query):
    try:
        speak(f"Searching YouTube for {query}", emotion='happy')
        pywhatkit.playonyt(query)
    except Exception as e:
        speak("Failed to play on YouTube", emotion='serious')
        print(e)

def search_wikipedia(query):
    try:
        result = pywhatkit.info(query, lines=2)
        speak(f"According to Wikipedia: {result}", emotion='neutral')
    except:
        speak("Could not find Wikipedia results", emotion='serious')

def open_app(app_name):
    try:
        # Try to open using Windows' default associations
        subprocess.Popen(f'start {app_name}', shell=True)
        speak(f"Opening {app_name}", emotion='happy')
    except Exception as e:
        speak(f"Couldn't open {app_name}", emotion='serious')

def close_app(app_name):
    try:
        # Close by window title
        os.system(f'taskkill /fi "WindowTitle eq {app_name}*" /f')
        speak(f"Closed {app_name}", emotion='happy')
    except:
        speak(f"Couldn't close {app_name}", emotion='serious')

def detect_wake_word():
    update_gui("🔇 Sleep mode - waiting for wake word")
    while True:
        command = listen(timeout=None)
        if command:
            # Check if command starts with any wake word
            for wake_word in WAKE_WORDS:
                if command.startswith(wake_word.lower()):
                    remaining_command = command[len(wake_word):].strip()
                    if remaining_command:  # If there's additional command after wake word
                        return remaining_command
                    speak("Yes Sir? How may I assist you?", emotion='neutral')
                    status_label.config(text="Status: Online", fg='green')
                    return True
            update_gui(f"[Ignored: '{command}']", is_user=False)

def process_command(command):
    normalized_cmd = command.lower().strip()
    
    if any(word in normalized_cmd for word in ["time", "what time"]):
        speak(f"The time is {datetime.now().strftime('%I:%M %p')}", emotion='neutral')
        
    elif any(word in normalized_cmd for word in ["date", "what day"]):
        speak(f"Today is {datetime.now().strftime('%A, %B %d')}", emotion='neutral')
        
    elif "good morning" in normalized_cmd:
        speak("Good morning, Sir. Systems at full capacity.", emotion='happy')
        
    elif "good night" in normalized_cmd:
        speak("Initiating sleep mode. Goodnight, Sir.", emotion='neutral')
        detect_wake_word()
    elif "play" in normalized_cmd and "youtube" in normalized_cmd:
        query = normalized_cmd.replace("play", "").replace("on youtube", "").strip()
        play_on_youtube(query)
        
    elif "wikipedia" in normalized_cmd:
        query = normalized_cmd.replace("wikipedia", "").replace("search", "").strip()
        search_wikipedia(query)

    # Application control
    elif any(word in normalized_cmd for word in ["open", "launch", "start"]):
        app_name_to_open = normalized_cmd.replace("open", "").replace("launch", "").replace("start", "").strip()
        open_app(app_name_to_open)

    elif any(word in normalized_cmd for word in ["close" , "terminate"]):
        app_name_to_close = normalized_cmd.replace("close", "").replace("terminate", "").strip()
        close_app(app_name_to_close)
        
    elif any(word in normalized_cmd for word in ["exit", "shutdown", "sleep"]):
        speak("Shutting down systems. Goodbye, Sir.", emotion='neutral')
        status_label.config(text="Status: Offline", fg='red')
        return False
        
    else:
        speak("Command not recognized. Please try again, Sir.", emotion='serious')
    return True

def jarvis_mode():
    global gui_running
    try:
        active = True
        while active:
            # First check if we got a combined wake+command
            result = detect_wake_word()
            
            if isinstance(result, str):  # We got a combined wake+command
                active = process_command(result)
            elif result is True:  # Just got wake word, now listen for command
                command = listen()
                if command:
                    active = process_command(command)
                    
    finally:
        gui_running = False
        audio_queue.put(None)
        pygame.mixer.quit()
        try:
            root.destroy()
        except:
            pass

if __name__ == "__main__":
    update_gui("""
    ╔════════════════════════════╗
    ║       J.A.R.V.I.S AI       ║
    ╚════════════════════════════╝
    """)
    
    # Run JARVIS in a separate thread so GUI doesn't freeze
    threading.Thread(target=jarvis_mode, daemon=True).start()

    # Run the GUI mainloop on the main thread
    root.mainloop()
