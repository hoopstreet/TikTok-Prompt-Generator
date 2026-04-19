import torch
from huggingface_hub import snapshot_download
from PIL import Image
import requests
from io import BytesIO

class MoondreamLoader:
    def __init__(self, model_id="hoopstreet/moondream3-preview", cache_dir="/tmp/model_cache"):
        self.model_id = model_id
        self.cache_dir = cache_dir
        self.model = None
    
    def load_model(self):
        print("Downloading model from Hugging Face...")
        local_path = snapshot_download(
            repo_id=self.model_id,
            cache_dir=self.cache_dir,
            local_files_only=False
        )
        print(f"Model downloaded to {local_path}")
        return local_path
    
    def load_image_from_url(self, url):
        response = requests.get(url, timeout=30)
        img = Image.open(BytesIO(response.content)).convert("RGB")
        return img
