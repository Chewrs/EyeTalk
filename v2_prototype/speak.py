import requests
import pygame
import time
from gtts import gTTS
import threading
import queue

# --- Base TTS class ---
class TTS:
    def __init__(self, engine='offline', lang='th'):
        pygame.mixer.init()
        self.engine = engine
        self.lang = lang

    def speak(self, text):
        if self.engine == 'online':
            self._speak_online(text)
        else:
            self._speak_offline(text)

    def _speak_online(self, text):
        lang = 'th-TH' if self.lang == 'th' else self.lang
        url = "https://translate.google.com/translate_tts"
        params = {"ie": "UTF-8", "q": text, "tl": lang, "client": "tw-ob"}
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, params=params, headers=headers)

        with open("temp.mp3", "wb") as f:
            f.write(response.content)

        pygame.mixer.music.load("temp.mp3")
        pygame.time.wait(500)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

    def _speak_offline(self, text):
        tts = gTTS(text=text, lang=self.lang, slow=False)
        tts.save("temp.mp3")
        pygame.mixer.music.load("temp.mp3")
        pygame.time.wait(500)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

# --- Queued version ---

class QueuedTTS:
    def __init__(self, engine='offline', lang='th', max_age=3):
        self.tts = TTS(engine=engine, lang=lang)
        self.queue = queue.Queue()
        self.max_age = max_age  # seconds
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        while True:
            timestamp, text = self.queue.get()
            age = time.time() - timestamp
            if age <= self.max_age:
                self.tts.speak(text)
            # else: skip because it's too old

    def speak(self, text):
        self.queue.put((time.time(), text))

