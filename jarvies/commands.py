from speech_engine import speak
from datetime import datetime
import pywhatkit, os, subprocess
from utils import get_time, get_date , set_reminder ,  set_alarm , cancel_alarm
from shortcut_sites import shortcut_sites
import re
import webbrowser
from browser_tools import get_weather 

def process_command(command):
    normalized_cmd = command.lower().strip()
    
    # Check for time-related commands
    if any(word in normalized_cmd for word in ["time", "what time"]):
        speak(f"The time is {get_time()}", emotion='neutral')
        
    # Check for date-related commands
    elif any(word in normalized_cmd for word in ["date", "what day"]):
        speak(f"Today is {get_date()}", emotion='neutral')
        
    # Respond to "good morning"
    elif "good morning" in normalized_cmd:
        speak("Good morning, Sir. Systems at full capacity.", emotion='happy')
        
    # Respond to "good night"
    elif "good night" in normalized_cmd:
        speak("Initiating sleep mode. security active remaining.  Goodnight, Sir.", emotion='neutral')
        return True
        
    # Play something on YouTube
    elif "play" in normalized_cmd and "youtube" in normalized_cmd:
        query = normalized_cmd.replace("play", "").replace("on youtube", "").strip()
        speak(f"Searching YouTube for {query}", emotion='happy')
        pywhatkit.playonyt(query)
        
    # Search Wikipedia
    elif "wikipedia" in normalized_cmd:
        query = normalized_cmd.replace("wikipedia", "").replace("search", "").strip()
        try:
            result = pywhatkit.info(query, lines=2)
            speak(f"According to Wikipedia: {result}", emotion='neutral')
        except:
            speak("Could not find Wikipedia results", emotion='serious')

    # Open websites or shortcut sites
    elif any(domain in normalized_cmd for domain in [".com", ".org", ".net", ".in"]) or \
         any(name in normalized_cmd for name in shortcut_sites):

        # First, try shortcut mapping
        for name, domain in shortcut_sites.items():
            if name in normalized_cmd:
                url = f"https://{domain}"
                speak(f"Opening {name}", emotion='happy')
                webbrowser.open(url)
                break
        else:
            # Fallback to regex if no shortcut matched
            match = re.search(r"(open|go to|visit)\s+(https?://)?(www\.)?([\w\.-]+\.\w+)", normalized_cmd)
            if match:
                site = match.group(4)
                url = f"https://{site}"
                speak(f"Opening {site}", emotion='happy')
                webbrowser.open(url)
            else:
                speak("Sorry, I couldn't understand the website.", emotion='serious')

    elif "weather" in normalized_cmd:
        get_weather("muzaffarnagar") # Replace with actual city or use an API

    # Handle reminders
    elif "remind me" in normalized_cmd or "set reminder" in normalized_cmd:
        set_reminder(normalized_cmd)


    # Open or launch applications
    elif any(word in normalized_cmd for word in ["open", "launch", "start"]):
        app_name_to_open = normalized_cmd.replace("open", "").replace("launch", "").replace("start", "").strip()
        subprocess.Popen(f'start {app_name_to_open}', shell=True)
        speak(f"Opening {app_name_to_open}", emotion='happy')


    # Handle alarm setting
    elif "set alarm" in normalized_cmd:
        match = re.search(r"set alarm for (.+)", normalized_cmd)
        if match:
                alarm_time = match.group(1).strip()
                set_alarm(alarm_time)
        else:
                speak("Please specify the time like 'set alarm for 7:30 am'", emotion='serious')

     # Handle alarm cancellation
    elif "cancel alarm" in normalized_cmd or "stop alarm" in normalized_cmd:
        cancel_alarm()


                
    # Handle exit, shutdown, or sleep commands
    elif any(word in normalized_cmd for word in ["exit", "shutdown", "sleep"]):
        speak("Shutting down systems. Goodbye, Sir.", emotion='neutral')
        from gui import status_label
        status_label.config(text="Status: Offline", fg='red')
        return False

    # Handle unrecognized commands
    else:
        speak("Command not recognized. Please try again, Sir.", emotion='serious')
    
    return True
