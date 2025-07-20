import torch
from torch.serialization import add_safe_globals
import torch.nn.modules.container as container
import ultralytics.nn.tasks as tasks
import ultralytics.nn.modules as modules

# Allow safe unpickling of required classes
add_safe_globals([tasks.DetectionModel, container.Sequential, modules.Conv])

from ultralyticsplus import YOLO, postprocess_classify_output

# Unsafe mode for trusted local file
orig_load = torch.load
torch.load = lambda *args, **kwargs: orig_load(*args, weights_only=False, **kwargs)

# Load model
model = YOLO('keremberke/yolov8s-scene-classification/best.pt')

# Set confidence threshold
model.overrides['conf'] = 0.25

# Set image
image = 'image.jpg'

# Predict
results = model.predict(image)
probs = results[0].probs.data
class_names = model.model.names

print("\nTop 5 Predictions:")
top_probs, top_idxs = probs.topk(5)
for i in range(5):
    idx = int(top_idxs[i])
    print(f"{class_names[idx]}: {top_probs[i].item():.4f}")

# ✅ Print all class probabilities
print("\nAll Class Probabilities:")
for i, prob in enumerate(probs):
    print(f"{class_names[i]}: {prob.item():.4f}")