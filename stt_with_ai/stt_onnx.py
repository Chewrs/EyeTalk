import onnxruntime as ort
import torchaudio
import numpy as np
from transformers import Wav2Vec2Processor


class ThaiASR:
    def __init__(self, model_path="wav2vec2_th.onnx", processor_path="processor"):
        # Load ONNX model and processor once
        self.session = ort.InferenceSession(model_path)
        self.processor = Wav2Vec2Processor.from_pretrained(processor_path)
        self.resampler = torchaudio.transforms.Resample(orig_freq=48000, new_freq=16000)  # adjustable if needed

    def transcribe(self, filename):
        # Load and resample audio
        speech_array, sr = torchaudio.load(filename)
        if sr != 16000:
            speech_array = self.resampler(speech_array)
        speech = speech_array[0].numpy()

        # Prepare input
        inputs = self.processor(speech, sampling_rate=16000, return_tensors="np", padding=True)
        input_values = inputs["input_values"]

        # Inference
        logits = self.session.run(["logits"], {"input_values": input_values.astype(np.float32)})[0]

        # Decode
        pred_ids = np.argmax(logits, axis=-1)
        return self.processor.batch_decode(pred_ids)[0]

