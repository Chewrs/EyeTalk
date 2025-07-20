from picamera2 import Picamera2
from time import sleep
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import time

# Setup model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
processor = BlipProcessor.from_pretrained("./blip_model")
model = BlipForConditionalGeneration.from_pretrained("./blip_model").to(device)

# Initialize camera
picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": (640, 360)})  # Use smaller size for speed
picam2.configure(config)
picam2.start()
sleep(1)

def caption_scene(image_path):
    raw_image = Image.open(image_path).convert('RGB')
    inputs = processor(raw_image, return_tensors="pt").to(device)
    generated_ids = model.generate(
        pixel_values=inputs.pixel_values,
        max_length=50,
        do_sample=True,
        top_k=120,
        top_p=0.9,
        early_stopping=True,
        num_return_sequences=1
    )
    result = processor.batch_decode(generated_ids, skip_special_tokens=True)
    return result[0]

try:
    while True:
        start = time.time()
        frame_path = "frame.jpg"
        picam2.capture_file(frame_path)
        print("Captured frame.")
        caption = caption_scene(frame_path)
        print(f"Caption: {caption}")
        print(f"Time taken: {time.time() - start:.2f} seconds")
        sleep(2)  # Wait 2 seconds before next frame (adjust as needed)

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    picam2.stop()