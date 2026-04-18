# TikTok-Prompt-Generator DNA 🧬

## 🚀 1. The Architecture (Weightless Deployment)
This project is designed for **"Zero-Local-Load"** development. Management happens on mobile (iPhone), while heavy lifting happens in the cloud.

* **Control Center (iSH iPhone):** The "Commander." Used for coding via terminal, Git management, and issuing version tags.
* **The Factory (GitHub Actions):** The "Builder." When a tag is pushed, it builds the Docker environment.
* **The Registry (Docker Hub):** The "Warehouse." Stores massive pre-baked AI model images.
* **The Storefront (Hugging Face):** The "Live App." Runs the Moondream 3 model on a T4 GPU for the end user.

## 🛠 2. Tool Purposes & Tech Stack
| Tool | Purpose | Tech Specs |
| :--- | :--- | :--- |
| **iSH (iPhone)** | Local terminal env to bypass the need for a PC. | Alpine Linux |
| **GitHub** | Version control and Automation hosting. | Git |
| **GitHub Actions** | CI/CD pipeline to build and sync deployments. | YAML Workflows |
| **Docker Hub** | Hosting pre-built images to avoid 20+ min build times on HF. | Docker Registry |
| **Hugging Face** | Hosting the production Gradio UI on free GPU. | T4 GPU (Small) |
| **Moondream 3** | Vision-language model to analyze video/images. | 9B Parameters |

## 🔗 3. Project Links
* **GitHub Repository:** https://github.com/hoopstreet/TikTok-Prompt-Generator
* **Docker Hub Registry:** https://hub.docker.com/r/hoopstreet/tiktok-prompt-generator
* **Hugging Face Space:** https://huggingface.co/spaces/hoopstreet/TikTok-Prompt-Generator

## 🔐 4. Variables & Secrets (GitHub Settings)
To make the automation work, the following **GitHub Actions Secrets** must be configured:
1.  `DOCKERHUB_USERNAME`: Your Docker Hub account name.
2.  `DOCKERHUB_TOKEN`: Personal Access Token from Docker Hub.
3.  `HF_TOKEN`: Write-access token from Hugging Face.

## 🤖 5. Dual-Action Workflow (GitHub Actions)
### Workflow 1: Build & Push (`docker-publish.yml`)
* **Purpose:** Compiles the heavy Python environment, Torch, and Moondream 3 weights into a Docker image.
* **Outcome:** Creates a versioned image like `v1.0.4` in Docker Hub.

### Workflow 2: Sync & Update HF (`hf-sync.yml`)
* **Purpose:** The "Auto-Editor." It edits the `hf.Dockerfile` on the fly to point to the new version and pushes it to Hugging Face.
* **Outcome:** Triggers an instant "reboot" on Hugging Face using the new pre-built image.

## ⌨️ 6. AI Developer Protocol (For AI/LLM Providers)
### The "Keyboard-less" Delivery Template
All AI providers must deliver code in the following structure for iSH compatibility:

**Part 1: Setup & Target (Summary)**
```bash
# [Number]. [Action Description]
echo "nameserver 8.8.8.8" > /etc/resolv.conf
cd ~/TikTok-Prompt-Generator
# [Specific Command: e.g., cat <<EOF > filename.ext]
# [Code Content]
# EOF
```

**Part 2: Execution & Sync**
```bash
# [Number]. Sync to Remote
git add .
git commit -m "update: [Specific Change]"
git push origin main
```

### Fundamental Rules:
1.  **NO MANUAL EDITS:** Never ask the user to open 'nano' or 'vi'.
2.  **DNS FIRST:** Every block involving Git or Network must start with `echo "nameserver 8.8.8.8" > /etc/resolv.conf`.
3.  **FRAGMENTATION:** If the code is >200 characters, split it into numbered steps (1, 2, 3) to avoid mobile clipboard crashes.
4.  **INSERTION PREFERENCE:** Use `sed` or `cat >>` to add logic to existing files instead of overwriting the whole file.

## 📌 7. Version History
* **v1.0.0 - v1.0.3:** Infrastructure stabilization and DNS fixes.
* **v1.0.4:** [STABLE] Master DNA Overhaul. Implemented AI Developer Protocol and Secret Documentation.

## 🧱 8. Original Repository Code Structure
- **Root Directory:**
    - `hf_moondream.py`: The Gradio app logic. Connects to Moondream 3.
    - `Dockerfile`: The "Heavy" build config for GitHub Actions. Includes Torch/CUDA.
    - `hf.Dockerfile`: The "Light" redirect config for Hugging Face Spaces.
    - `deploy.sh`: Local automation script for versioning and DNS resolution.
    - `DNA.md`: This master documentation file.
    - `README.md`: Public-facing project overview (auto-synced with DNA).
- **.github/workflows/:**
    - `docker-publish.yml`: Manages the Docker Hub image build on tags.
    - `hf-sync.yml`: Manages the auto-editing and syncing to Hugging Face.

## ⚙️ 9. Full Project Setup Details
### Mobile Initialization (iSH)
1. **DNS Fix**: `echo "nameserver 8.8.8.8" > /etc/resolv.conf`
2. **Git Setup**: `git init`, then `git remote add origin [URL]`
3. **Permissions**: `chmod +x deploy.sh`

### Cloud Initialization (GitHub)
1. **Secrets**: Populate `DOCKERHUB_*` and `HF_TOKEN` in Settings > Secrets.
2. **Space Creation**: Set up a Hugging Face Space using the "Docker" SDK.
3. **Linkage**: Ensure the HF Space name matches the one defined in `hf-sync.yml`.
* **v1.0.5:** [STABLE] Preparing TikTok-specific Taglish prompt logic.

## 📂 10. Complete Source Inventory
### 🧠 AI Logic & Entry Points
- `hf_moondream.py`: Primary Gradio UI (Production).
- `moondream.py`: Local model interface.
- `vision.py`, `text.py`, `layers.py`, `rope.py`, `utils.py`: Core model architecture components.
- `lora.py`, `region.py`, `image_crops.py`: Advanced inference and fine-tuning utilities.

### 🏋️ Model Weights (The Heavy Lifting)
- `model-0000x-of-00004.safetensors`: Sharded model weights (v1/v2).
- `model_fp8.pt`: Quantized model weights for performance.
- `config.json`, `config.py`: Model configuration and hyper-parameters.

### 🖼 Assets & Docs
- `DNA.md`, `README.md`, `LICENSE.md`: Documentation suite.
- `*.png`: Visual demonstration assets (Visual reasoning, region detection).

### 🛠 Deployment Files
- `deploy.sh`: The iSH Controller script.
- `Dockerfile`: The Factory (GitHub/Docker Hub) instructions.
- `hf.Dockerfile`: The Space (Hugging Face) redirect instructions.
- `.github/workflows/`: Automation engine.

## 📄 11. Exhaustive Repository Manifest (Full List)
### ⚙️ Core System & Infrastructure
- `.github/workflows/`: CI/CD automation logic.
- `.gitattributes`: Git LFS and file handling rules.
- `DNA.md`: Master project blueprint and protocol.
- `README.md`: Main repository documentation.
- `LICENSE.md`: Legal and usage permissions.
- `deploy.sh`: Mobile controller script for iSH.
- `Dockerfile`: Primary build instructions (Docker Hub).
- `hf.Dockerfile`: Redirect instructions (Hugging Face).

### 🧠 Model Architecture & Logic
- `hf_moondream.py`: Gradio production entry point.
- `moondream.py`: Core model class definition.
- `config.json` / `config.py`: Model configuration settings.
- `vision.py` / `text.py`: Modality-specific logic.
- `layers.py` / `rope.py` / `utils.py`: Transformer components.
- `lora.py` / `region.py` / `image_crops.py`: Specialized inference tools.

### 🏋️ Weights & Data (High Volume)
- `model-00001-of-00004.safetensors`
- `model-00002-of-00004.safetensors`
- `model-00003-of-00004.safetensors`
- `model-00004-of-00004.safetensors`
- `model.safetensors.index.json`: Weight mapping index.
- `model_fp8.pt`: Quantized performance weights.
- `modelv2-00001-of-00004.safetensors`
- `modelv2-00002-of-00004.safetensors`
- `modelv2-00003-of-00004.safetensors`
- `modelv2-00004-of-00004.safetensors`

### 🖼 Visual Demonstration Assets
- `open_vocab_detect.png`
- `point_count.png`
- `region.png`
- `structured_outputs.png`
- `visual_reasoning.png`
* **v1.0.6:** [STABLE] Implementing Taglish Video Script templates in hf_moondream.py.
* **v1.0.7:** [STABLE] Fixed Dual-Action Workflow (Main/Tag) and clean HF Sync logic.
v1.0.8: [STABLE] Workflow syntax fix (Literal EOF protection).
v1.0.9: [STABLE] Finalized Weightless Build: Strict version tagging, removed 'latest' bloat, and cleaned HF metadata.
v1.1.0: [CURRENT] Scaling TikTok Automation: Multi-product batch processing logic.
v1.1.3: [STABLE] Infrastructure Gold - Absolute Imports v1.1.3: [CURRENT] Torch 2.5.1 Deployment Global removal of relative imports to fix 'no known parent package' error.
v1.1.3: [STABLE] Final Infrastructure Gold release. Fully mobile-manageable. Absolute imports validated.

## v1.1.5: [AUTO] Mobile Release
- Timestamp: 2026-04-18 20:19
- Source: iSH Mobile Deploy
- Notes:
  - Auto-commit from mobile
  - Synced with GitHub Actions
  - Triggered Docker + HF pipeline


## v1.1.6: [AUTO] Mobile Release
- Timestamp: 2026-04-18 20:19
- Source: iSH Mobile Deploy
- Notes:
  - Auto-commit from mobile
  - Synced with GitHub Actions
  - Triggered Docker + HF pipeline

