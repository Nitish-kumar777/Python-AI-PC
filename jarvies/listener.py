import speech_recognition as sr
from gui import status_label, update_gui
from config import WAKE_WORDS
from speech_engine import speak
from commands import process_command
from config import gui_running
import pygame

def listen(timeout=8, phrase_time_limit=10):
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
        except:
            return None

def detect_wake_word():
    update_gui("🔇 Sleep mode - waiting for wake word")
    while True:
        command = listen(timeout=None)
        if command:
            for wake_word in WAKE_WORDS:
                if command.startswith(wake_word.lower()):
                    remaining_command = command[len(wake_word):].strip()
                    if remaining_command:
                        return remaining_command
                    speak("Yes Sir? How may I assist you?", emotion='neutral')
                    status_label.config(text="Status: Online", fg='green')
                    return True
            update_gui(f"[Ignored: '{command}']", is_user=False)

def jarvis_mode():
    try:
        active = True
        while active:
            result = detect_wake_word()
            if isinstance(result, str):
                active = process_command(result)
            elif result is True:
                command = listen()
                if command:
                    active = process_command(command)
    finally:
        global gui_running
        gui_running = False
        from config import audio_queue
        audio_queue.put(None)
        pygame.mixer.quit()
        from gui import root
        try:
            root.destroy()
        except:
            pass
