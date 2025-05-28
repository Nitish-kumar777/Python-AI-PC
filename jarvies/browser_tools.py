import requests
import webbrowser
import os
from speech_engine import speak  
from dotenv import load_dotenv

load_dotenv()

def open_app_with_browser(url):
    try:
        webbrowser.open(url)
        speak(f"Opening {url}", emotion='happy')
    except Exception as e:
        speak("Failed to open the browser", emotion='serious')
        print(e)

def get_weather(city="muzaffarnagar"):
    api_key = os.getenv("WEATHER_API_KEY")  # KEY NAME MATCH KAREIN
    if not api_key:
        speak("Weather API key not found in environment variables.", emotion='serious')
        return
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url).json()
        if response.get("cod") != 200:
            speak(f"Couldn't find weather data for {city}", emotion='serious')
            return
        
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp}°C with {desc}", emotion='neutral')

    except Exception as e:
        speak("Sorry, I couldn't get the weather data", emotion='serious')
        print(f"[ERROR] {e}")