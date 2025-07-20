from speak import QueuedTTS,TTS
import os
import time
from gtts import gTTS
import subprocess

from pydub import AudioSegment
from pydub.playback import play
import tempfile

from geminivisionhelper import GeminiVisionHelper


def test_tts(text):
    start = time.time()
    tts = TTS(engine='offline', lang='th')  # Initialize TTS with offline engine and Thai language


    tts.speak(text)  # Test with Thai text
    print(f"Time taken for TTS:{ time.time() - start:.4f}  {text}")


#test_tts("อันนี้เป็นสิ่งที่ฉันเห็น ฉันเห็นบ้านหลังใหญ่มีคนอยู๋หลายคน")
#play_sound('month.mp3')
start_everything = time.time()

GeminiVisionHelper = GeminiVisionHelper()
text = "ข้างหน้ามีคนไหม"
print(GeminiVisionHelper.describe_image())

print(f"Total time taken: {time.time() - start_everything:.4f} seconds")