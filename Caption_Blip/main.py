import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import time
start = time.time() 
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the BLIP model and processor
processor = BlipProcessor.from_pretrained("./blip_model")
model = BlipForConditionalGeneration.from_pretrained("./blip_model").to(device)


def caption_scene(image_path, processor, model):
    
    raw_image = Image.open(image_path).convert('RGB')

    
    inputs = processor(raw_image, return_tensors="pt")
    pixel_values = inputs.pixel_values.to(device)

    generated_ids = model.generate(pixel_values=pixel_values, max_length=50,
                do_sample=True,
                top_k=120,
                top_p=0.9,
                early_stopping=True,
                num_return_sequences=1)

    result = processor.batch_decode(generated_ids, skip_special_tokens=True)
    print(result)
    end = time.time()
    print(f"Time taken: {end - start}")


