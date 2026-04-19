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
        self.processor = None
    
    def load_model(self):
        """Downloads model from HF Hub (only once) and loads into memory"""
        # Download weights from your model repo
        local_path = snapshot_download(
            repo_id=self.model_id,
            cache_dir=self.cache_dir,
            local_files_only=False  # Downloads from HF
        )
        
        # Import moondream (your custom version or original)
        from moondream import MoondreamModel, VisionEncoder
        
        # Load with FP8 for memory efficiency on free GPU
        self.model = MoondreamModel.from_pretrained(
            local_path,
            torch_dtype=torch.float8_e4m3fn,  # FP8 for memory
            device_map="auto"
        )
        return self.model
    
    def load_image_from_url(self, url):
        """Downloads image from URL and processes it"""
        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGB")
        return img
