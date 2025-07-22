import requests
#import pygame
import time
from gtts import gTTS
import threading
import queue
import subprocess

# --- Base TTS class ---
class TTS:
    def __init__(self, engine='offline', lang='th'):
        #pygame.mixer.init()
        self.engine = engine
        self.lang = lang

    def speak(self, text, file_path="speech.mp3",play=True,speed = 2.0):
        if self.engine == 'online':
            self._speak_online(text, file_path)
            if play:
                self._subprocess_play(file_path, speed)
        else:
            self._TTS_offline(text, file_path)
            if play:
                self._subprocess_play(file_path, speed)

    def _TTS_online(self, text,file_path):
        lang = 'th-TH' if self.lang == 'th' else self.lang
        url = "https://translate.google.com/translate_tts"
        params = {"ie": "UTF-8", "q": text, "tl": lang, "client": "tw-ob"}
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, params=params, headers=headers)

        with open(file_path, "wb") as f:
            f.write(response.content)

    def _TTS_offline(self, text,file_path):
        tts = gTTS(text=text, lang=self.lang, slow=False)
        tts.save(file_path)

    #play music with pygame
    '''
    def _pygame_play(self, file_path):
        pygame.mixer.music.load(file_path)
        pygame.time.wait(500)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue'''
    
    #play music with ffplay via subprocess(terminal)
    def _subprocess_play(self, file_path,speed):
        subprocess.run(['ffplay', '-nodisp', '-autoexit', '-af', f'atempo={speed}', file_path])


# --- Queued version ---

class QueuedTTS:
    def __init__(self, engine='offline', lang='th', max_age=2):
        self.tts = TTS(engine=engine, lang=lang)
        self.queue = queue.Queue()
        self.max_age = max_age  # seconds
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        while True:
            timestamp, text,file_path = self.queue.get()
            age = time.time() - timestamp
            if age <= self.max_age:
                self.tts.speak(text,file_path)  # Play immediately if within max_age
            # else: skip because it's too old

    def speak(self, text,file_path="speech.mp3", play=True,speed = 2.0):
        self.queue.put((time.time(), text,file_path))

