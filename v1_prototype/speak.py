import requests
import pygame
import time
from gtts import gTTS

class TTS:
    def __init__(self, engine='offline', lang='th'):
        pygame.mixer.init()
        self.engine = engine
        self.lang = lang

    def speak(self, text):
        if self.engine == 'online':
            self._speak_online(text)
        else:
            return self._speak_offline(text)

    def _speak_online(self, text):
        lang = 'th-TH' if self.lang == 'th' else self.lang  # Ensure lang is in correct format
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
        start = time.time()
        tts = gTTS(text=text, lang=self.lang, slow=False)
        tts.save("temp.mp3")



        pygame.mixer.music.load("temp.mp3")
        pygame.time.wait(500)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

