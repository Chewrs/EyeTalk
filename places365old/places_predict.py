import time
start = time.time()
import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image

start_after_import = time.time()

# Load class labels
with open('categories_places365.txt') as f:
    classes = [line.strip().split(' ')[0][3:] for line in f]

# Load the ResNet18 model
model = models.resnet18(num_classes=365)
checkpoint = torch.load('resnet18_places365.pth.tar', map_location='cpu')
state_dict = {k.replace('module.', ''): v for k, v in checkpoint['state_dict'].items()}
model.load_state_dict(state_dict)
model.eval()

# Preprocessing steps
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406], 
        std=[0.229, 0.224, 0.225])
])

# Load your own image
image_path = 'image.jpg'  # <-- Put your image in the same folder
img = Image.open(image_path).convert('RGB')
input_tensor = transform(img).unsqueeze(0)

# Predict
with torch.no_grad():
    output = model(input_tensor)
    probs = torch.nn.functional.softmax(output[0], dim=0)

# Show top 5 results
top5 = torch.topk(probs, 5)
print("Top 5 Scene Predictions:")
for i in range(5):
    idx = top5.indices[i].item()
    print(f"{classes[idx]}: {top5.values[i].item():.4f}")

print(f"Time taken after import: {time.time() - start_after_import:.2f} seconds")
print(f"Time taken overall: {time.time() - start:.2f} seconds")
