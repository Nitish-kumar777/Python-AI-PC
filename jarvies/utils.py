# utils.py
from datetime import datetime
import re
import threading
import pywhatkit
import subprocess
import os
from speech_engine import speak
import time
from playsound import playsound

alarm_cancel_flag = {"cancel": False}

def get_time():
    return datetime.now().strftime("%I:%M %p")

def get_date():
    return datetime.now().strftime("%A, %B %d, %Y")

def play_on_youtube(query):
    from speech_engine import speak
    try:
        speak(f"Searching YouTube for {query}", emotion='happy')
        pywhatkit.playonyt(query)
    except Exception as e:
        speak("Failed to play on YouTube", emotion='serious')
        print(e)

def search_wikipedia(query):
    from speech_engine import speak
    try:
        result = pywhatkit.info(query, lines=2)
        speak(f"According to Wikipedia: {result}", emotion='neutral')
    except:
        speak("Could not find Wikipedia results", emotion='serious')

def open_app(app_name):
    from speech_engine import speak
    try:
        subprocess.Popen(f'start {app_name}', shell=True)
        speak(f"Opening {app_name}", emotion='happy')
    except Exception as e:
        speak(f"Couldn't open {app_name}", emotion='serious')

def close_app(app_name):
    from speech_engine import speak
    try:
        os.system(f'taskkill /fi "WindowTitle eq {app_name}*" /f')
        speak(f"Closed {app_name}", emotion='happy')
    except:
        speak(f"Couldn't close {app_name}", emotion='serious')

def set_reminder(command):
    from speech_engine import speak  # Safe from circular import
    match = re.search(r"(\d+)\s*(minute|minutes|second|seconds)", command)
    if match:
        value = int(match.group(1))
        unit = match.group(2)

        delay = value * 60 if "minute" in unit else value

        message_match = re.search(r"to (.+)", command)
        reminder_message = message_match.group(1) if message_match else "your reminder"

        speak(f"Setting a reminder in {value} {unit} to {reminder_message}", emotion='neutral')

        def reminder():
            speak(f"Reminder alert: {reminder_message}", emotion='happy')

        threading.Timer(delay, reminder).start()
    else:
        speak("Please tell me how long to wait, like 'in 2 minutes'", emotion='serious')


def set_alarm(alarm_time):
    def alarm_thread():
        try:
            cleaned_time = alarm_time.lower().replace(".", "").replace("a m", "am").replace("p m", "pm").replace(" ", "")
            cleaned_time = re.sub(r"(am|pm)", r" \1", cleaned_time)

            alarm_time_clean = datetime.strptime(cleaned_time, "%I:%M %p").strftime("%H:%M")
            speak(f"Alarm set for {alarm_time_clean}", emotion='neutral')

            while True:
                if alarm_cancel_flag["cancel"]:
                    speak("Alarm cancelled, Sir.", emotion='neutral')
                    alarm_cancel_flag["cancel"] = False
                    return

                now = datetime.now().strftime("%H:%M")
                if now == alarm_time_clean:
                    speak("⏰ Alarm ringing, Sir! Wake up or continue domination.", emotion='happy')
                    playsound("assets/alarm.mp3")  # Change path if needed
                    break

                time.sleep(10)

        except Exception as e:
            speak("Sorry, I couldn't understand the alarm time format.", emotion='serious')
            print("Alarm Error:", e)

    threading.Thread(target=alarm_thread, daemon=True).start()

def cancel_alarm():
    alarm_cancel_flag["cancel"] = True