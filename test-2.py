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