from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="keremberke/yolov8s-scene-classification",
    local_dir="keremberke/yolov8s-scene-classification",
    local_dir_use_symlinks=False  # ensures full copy, no symlinks
)
