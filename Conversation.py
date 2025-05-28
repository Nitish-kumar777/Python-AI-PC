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
import sys
import subprocess

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Constants
WAKE_WORDS = ["jarvis", "hey jarvis", "wake up"]
SAMPLE_RATE = 16000
CHUNK_SIZE = 480

# Global flag for GUI state
gui_running = True

# Audio queue for non-blocking playback
audio_queue = queue.Queue()

# Create GUI
root = tk.Tk()
root.title("J.A.R.V.I.S AI System")
root.geometry("600x400")
root.configure(bg='#0a0a1a')

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, 
                                    bg='#0a0a1a', fg='#00ff00', 
                                    font=('Courier New', 12))
text_area.pack(pady=20)
text_area.insert(tk.INSERT, "Initializing J.A.R.V.I.S systems...\n")
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

# 💬 Non-blocking Speak function with threading
def speak(text, lang='en', emotion='neutral'):
    update_gui(text)
    print("⌛ Generating audio...")
    
    def _speak():
        try:
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
                temp_path = tmp_file.name
            
            # Adjust speech parameters based on emotion
            if emotion == 'happy':
                tts = gTTS(text=text, lang=lang, tld='co.uk', slow=False)
            elif emotion == 'serious':
                tts = gTTS(text=text, lang=lang, tld='co.uk', slow=True)
            else:  # neutral
                tts = gTTS(text=text, lang=lang, tld='co.uk', slow=False)
            
            tts.save(temp_path)
            audio_queue.put(temp_path)
            
        except Exception as e:
            print("Error in speech synthesis:", e)
    
    thread = threading.Thread(target=_speak)
    thread.start()

# Audio playback thread
def audio_player():
    while True:
        audio_file = audio_queue.get()
        if audio_file is None:  # Exit signal
            break
            
        try:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
        finally:
            # Ensure file is closed before deletion
            pygame.mixer.music.stop()
            try:
                if os.path.exists(audio_file):
                    os.unlink(audio_file)
            except PermissionError:
                # If still locked, schedule deletion later
                threading.Timer(1.0, lambda: os.unlink(audio_file) if os.path.exists(audio_file) else None).start()
                
        audio_queue.task_done()

# Start audio player thread
player_thread = threading.Thread(target=audio_player)
player_thread.daemon = True
player_thread.start()

# 🎧 Improved Listen function
def listen(timeout=5, phrase_time_limit=10):
    r = sr.Recognizer()
    r.energy_threshold = 4000
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8
    
    with sr.Microphone() as source:
        update_gui("🔕 Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)
        update_gui("🎙️ Listening...")
        status_label.config(text="Status: Listening", fg='yellow')
        
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            status_label.config(text="Status: Processing", fg='orange')
            
            command = r.recognize_google(audio, language='en-in').lower()
            update_gui(command, is_user=True)
            return command
            
        except sr.WaitTimeoutError:
            status_label.config(text="Status: Standby", fg='green')
            return None
        except sr.UnknownValueError:
            update_gui("Could not understand audio", is_user=False)
            status_label.config(text="Status: Standby", fg='green')
            return None
        except sr.RequestError as e:
            update_gui(f"Error with speech service: {e}", is_user=False)
            status_label.config(text="Status: Error", fg='red')
            return None

# 🔍 Wake word detection
def detect_wake_word():
    update_gui("🛌 In sleep mode. Waiting for wake word...")
    while True:
        command = listen(timeout=None)
        if command and any(wake_word in command for wake_word in WAKE_WORDS):
            speak("Systems online. How may I assist you?", emotion='happy')
            return True

# 🕒 Datetime functions
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

# 🤖 Enhanced J.A.R.V.I.S mode
def jarvis_mode():
    global gui_running
    speak("All systems operational. Online and ready, Sir.", emotion='happy')
    status_label.config(text="Status: Online", fg='green')
    
    try:
        while True:
            cmd = listen()
            if cmd:
                normalized_cmd = re.sub(r'[^\w\s]', '', cmd).strip()
                
                # Time commands
                if any(word in normalized_cmd for word in ["time", "what time"]):
                    speak(f"The current time is {get_time()}", emotion='neutral')
                    
                # Date commands
                elif any(word in normalized_cmd for word in ["date", "what day", "today"]):
                    speak(f"Today is {get_date()}", emotion='neutral')
                    
                # Wake commands
                elif any(word in normalized_cmd for word in ["wake up", "activate", "hello"]):
                    speak("Systems at full capacity. How may I assist you today, Sir?", emotion='happy')
                    
                # Greetings
                elif "good morning" in normalized_cmd:
                    speak(f"Good morning, Sir. The time is {get_time()}. Your schedule appears light today.", emotion='happy')
                    
                elif "good night" in normalized_cmd:
                    speak("Good night, Sir. Initiating sleep protocols. Security systems will remain active.", emotion='neutral')
                    time.sleep(2)
                    detect_wake_word()
                    
                # Emotional responses
                elif any(word in normalized_cmd for word in ["love you", "i love you"]):
                    speak("While I lack human emotions, I am programmed to prioritize your needs above all else, Sir.", emotion='happy')
                    
                # Status check
                elif any(phrase in normalized_cmd for phrase in ["how are you", "how you doing"]):
                    responses = [
                        "All systems functioning optimally, Sir.",
                        "Diagnostics show 100% operational capacity.",
                        "I am operating at peak efficiency, ready to assist you."
                    ]
                    speak(random.choice(responses), emotion='happy')
                    
                # Gratitude
                elif any(word in normalized_cmd for word in ["thank you", "thanks"]):
                    responses = [
                        "You're most welcome, Sir.",
                        "My pleasure to serve.",
                        "Always at your service."
                    ]
                    speak(random.choice(responses), emotion='happy')
                    
                # Media control
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
                # Exit commands
                elif any(word in normalized_cmd for word in ["exit", "shut down" , "shutdown", "sleep", "goodbye"]):
                    speak("Initiating shutdown sequence. Security systems will remain active. Goodbye, Sir.", emotion='neutral')
                    status_label.config(text="Status: Offline", fg='red')
                    return
                    
                # Identity
                elif any(phrase in normalized_cmd for phrase in ["who are you", "your name"]):
                    speak("I am J.A.R.V.I.S, an artificial intelligence created to assist you, Sir. "
                         "Just Another Rather Very Intelligent System.", emotion='neutral')
                    
                else:
                    speak(f"I heard: '{cmd}'. Would you like to rephrase that, Sir?", emotion='serious')
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
    ║  Just Another Rather Very  ║
    ║    Intelligent System      ║
    ╚════════════════════════════╝
    """)
    
    # Start with wake word detection
    detect_wake_word()
    jarvis_mode()
    
    root.mainloop()