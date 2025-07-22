import time
from stt_onnx import ThaiASR
from record import AudioRecorder
from geminivisionhelper import GeminiVisionHelper
from speak import TTS, QueuedTTS
from camera_handler import CameraHandler

import threading

# Init
tts = TTS(engine='offline', lang='th')  
Qtts = QueuedTTS(engine='offline', lang='th')  # Queued TTS

recorder = AudioRecorder() 
stt = ThaiASR() 
helper = GeminiVisionHelper()  #ai
camera = CameraHandler() #picamera2

def capture_image(image_path = "Images/image.jpg"):
    camera.capture_image(image_path)


tts._subprocess_play('effect/samsung_notification.mp3',speed=1.0)
try:
    while True:
        input("🎙 Press Enter to record...") #wait for pressing Enter
        tts._subprocess_play('effect/click-high.mp3',speed=2.0)
        image_path = "Images/image.jpg"
        threading.Thread(target=capture_image, args=(image_path,)).start() #Capture image(in the background)

        start = time.time()
        recorder.record_and_save(duration=5)  # Record for x seconds and save as 'record.wav'
        text = stt.transcribe("record.wav") # Transcribe the record.wav' audio to text
        print("🗣️", text)
        Qtts.speak(f"คุณพูดว่า {text} ฉันขอดูแป๊บนึงนะ")  #in the background

        print(f"Time taken: {time.time() - 5 - start:.2f} seconds")
        output = helper.describe_image(image_path=image_path,prompt = text) # Describe the via Gemini api 
        print(output)
        tts.speak(output)  #Speak the output

finally:
    camera.close()
    print("Camera handler closed.")

