from gtts import gTTS
from config import audio_queue
import tempfile, pygame, time, threading, os
from gui import update_gui

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

threading.Thread(target=audio_player, daemon=True).start()
