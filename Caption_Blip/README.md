# BLIP Image Captioning

This script uses the BLIP model to generate a caption scene for an image.

## Installation

Start an env
```
python3 -m venv env
```
```
source env/bin/activate
```

Install requirement libraries
```
pip install torch torchvision transformers pillow requests
```
Use this command if you don’t have a GPU or want to run on CPU only:
```
pip install torch --index-url https://download.pytorch.org/whl/cpu
```
## Setup

1. Download the BLIP model to `./blip_model`:

```
python3 download_model.py
```

2. Add an image name image.jpg in the same folder, or capture by:
```
python3 capture_in_env.py
```

## Run
```
python3 main.py
```

### Output

['a dog running on the grass']


Time taken: 2.15

