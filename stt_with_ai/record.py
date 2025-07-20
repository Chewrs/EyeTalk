import sounddevice as sd
from scipy.io.wavfile import write
import subprocess

class AudioRecorder:
    def __init__(self, filename='record.wav', default_duration=5, sample_rate=16000):
        self.filename = filename
        self.default_duration = default_duration
        self.sample_rate = sample_rate

    def record_and_save(self, duration=None):
        duration = duration if duration is not None else self.default_duration
        print(f"Recording for {duration} seconds...")
        audio = sd.rec(int(duration * self.sample_rate),
                       samplerate=self.sample_rate,
                       channels=1, dtype='int16')
        sd.wait()
        write(self.filename, self.sample_rate, audio)
        print(f"Saved as {self.filename}")

    def play(self):
        print(f"Playing {self.filename}...")
        subprocess.run(f"aplay {self.filename}", shell=True)



