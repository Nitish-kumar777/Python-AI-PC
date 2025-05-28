import pygame
import queue

# Audio and Wakeword
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
WAKE_WORDS = ["jarvis", "hey jarvis", "wake up"]
SAMPLE_RATE = 16000
CHUNK_SIZE = 512

# Shared variables
gui_running = True
audio_queue = queue.Queue()
