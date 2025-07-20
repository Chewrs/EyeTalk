 
---
tags:
- ultralyticsplus
- yolov8
- ultralytics
- yolo
- vision
- image-classification
- pytorch
- awesome-yolov8-models
library_name: ultralytics
library_version: 8.0.20
inference: false

datasets:
- keremberke/indoor-scene-classification

model-index:
- name: keremberke/yolov8s-scene-classification
  results:
  - task:
      type: image-classification

    dataset:
      type: keremberke/indoor-scene-classification
      name: indoor-scene-classification
      split: validation

    metrics:
      - type: accuracy
        value: 0.02375  # min: 0.0 - max: 1.0
        name: top1 accuracy
      - type: accuracy
        value: 0.08986  # min: 0.0 - max: 1.0
        name: top5 accuracy
---

<div align="center">
  <img width="640" alt="keremberke/yolov8s-scene-classification" src="https://huggingface.co/keremberke/yolov8s-scene-classification/resolve/main/thumbnail.jpg">
</div>

### Supported Labels

```
['airport_inside', 'artstudio', 'auditorium', 'bakery', 'bookstore', 'bowling', 'buffet', 'casino', 'children_room', 'church_inside', 'classroom', 'cloister', 'closet', 'clothingstore', 'computerroom', 'concert_hall', 'corridor', 'deli', 'dentaloffice', 'dining_room', 'elevator', 'fastfood_restaurant', 'florist', 'gameroom', 'garage', 'greenhouse', 'grocerystore', 'gym', 'hairsalon', 'hospitalroom', 'inside_bus', 'inside_subway', 'jewelleryshop', 'kindergarden', 'kitchen', 'laboratorywet', 'laundromat', 'library', 'livingroom', 'lobby', 'locker_room', 'mall', 'meeting_room', 'movietheater', 'museum', 'nursery', 'office', 'operating_room', 'pantry', 'poolinside', 'prisoncell', 'restaurant', 'restaurant_kitchen', 'shoeshop', 'stairscase', 'studiomusic', 'subway', 'toystore', 'trainstation', 'tv_studio', 'videostore', 'waitingroom', 'warehouse', 'winecellar']
```

### How to use

- Install [ultralyticsplus](https://github.com/fcakyon/ultralyticsplus):

```bash
pip install ultralyticsplus==0.0.21
```

- Load model and perform prediction:

```python
from ultralyticsplus import YOLO, postprocess_classify_output

# load model
model = YOLO('keremberke/yolov8s-scene-classification')

# set model parameters
model.overrides['conf'] = 0.25  # model confidence threshold

# set image
image = 'https://github.com/ultralytics/yolov5/raw/master/data/images/zidane.jpg'

# perform inference
results = model.predict(image)

# observe results
print(results[0].probs) # [0.1, 0.2, 0.3, 0.4]
processed_result = postprocess_classify_output(model, result=results[0])
print(processed_result) # {"cat": 0.4, "dog": 0.6}
```

**More models available at: [awesome-yolov8-models](https://yolov8.xyz)**