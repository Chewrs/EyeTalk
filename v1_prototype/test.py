import time
from gtts import gTTS
import pygame
import threading
import queue
start = time.time()
pygame.mixer.init()

tts_queue = queue.Queue()
play_lock = threading.Lock()

def generate_tts(text, lang='th', filename='temp.mp3'):
    start = time.time()
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(filename)
    return time.time() - start

def play_tts(filename):
    play_lock.acquire()
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    finally:
        play_lock.release()

def speak(text, lang='th', index=0):
    filename = f"temp_{index}.mp3"
    gen_time = generate_tts(text, lang, filename)
    tts_queue.put((filename, gen_time))

def play_worker():
    while True:
        filename, gen_time = tts_queue.get()
        play_start = time.time()
        play_tts(filename)
        play_time = time.time() - play_start
        total_time = gen_time + play_time
        tts_queue.task_done()

# Start playback thread
threading.Thread(target=play_worker, daemon=True).start()

# Example usage
speak("สวัสดีครับ เป็นวันที่ดีและมีความดีเกิดขึ้นมากกว่า", index=1)
speak("วันนี้อากาศดี ดีจริงไหมต้องรอดูไปก่อน", index=2)
speak("ขอบคุณครับ ที่ได้ช่วยเหลือกันมาโดยตลอด", index=3)

# Wait for all TTS to play
tts_queue.join()

print("Total time taken:", time.time() - start)