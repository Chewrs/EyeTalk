from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="michelecafagna26/blip-base-captioning-ft-hl-scenes",
    local_dir="blip_model",
    local_dir_use_symlinks=False  # ensures full copy, no symlinks
)