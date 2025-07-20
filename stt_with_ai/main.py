from stt_onnx import ThaiASR
from record import AudioRecorder
from geminivisionhelper import GeminiVisionHelper
import time
from speak import TTS, QueuedTTS
from camera_handler import CameraHandler

# Init
tts = TTS(engine='offline', lang='th')  
Qtts = QueuedTTS(engine='offline', lang='th')  # Queued TTS

recorder = AudioRecorder() 
stt = ThaiASR() 
helper = GeminiVisionHelper()  #ai
camera = CameraHandler() #picamera2




try:
    while True:
        input("🎙 Press Enter to record...") #wait for pressing Enter
        tts.speak("เริ่มพูดได้เลย")
        image_path = "Images/image.jpg"
        camera.capture_image(image_path)
        print("capture image")
        start = time.time()
        recorder.record_and_save(duration=5)  # Record for 3 seconds and save as 'record.wav'
        text = stt.transcribe("record.wav") # Transcribe the recorded audio to text
        print("🗣️", text)
        Qtts.speak(f"คุณพูดว่า {text} ฉันขอดูแป๊บนึงนะ")  

        print(f"Time taken: {time.time() - 5 - start:.2f} seconds")
        output = helper.describe_image(image_path=image_path,prompt = text) # Describe the via Gemini api 
        print(output)
        tts.speak(output)  #Speak the output

finally:
    camera.close()
    print("Camera handler closed.")

