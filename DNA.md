# TikTok-Prompt-Generator DNA 🧬

## 🚀 The Architecture (Weightless Deployment)
This project is designed to be managed entirely from a mobile environment (iSH on iPhone) and deployed to high-performance GPU environments without a local VPS.

1.  **Control Center (iSH):** Code editing, Git operations, and version tagging.
2.  **Automation (GitHub Actions):** Triggered by tags (`v*`). Builds and pushes Docker images.
3.  **Registry (Docker Hub):** Stores pre-built images with versioned tags (`v1.x.x`).
4.  **Deployment (Hugging Face Spaces):** Pulls the pre-built image to run **Moondream 3** on a free T4 GPU.

## 🛠 Tech Stack
- **Vision Model:** Moondream 3 (9B Parameters)
- **Runtime:** Python 3.10-slim
- **Infrastructure:** Docker (CI/CD via GitHub Actions)
- **Local Env:** Alpine Linux (iSH)

## 📌 Version History
- **v1.0.0:** Initial Setup.
- **v1.0.1:** Added Moondream 3 dependencies.
- **v1.0.2:** Infrastructure refactor.
- **v1.0.3:** **[CURRENT]** Fixed Dockerfile renaming and stabilized iSH-to-GitHub pipeline.

## 📡 Deployment Commands (Internal)
To deploy a new version from iSH:
`./deploy.sh v1.x.x`

## 🔗 Project Links
- **GitHub:** https://github.com/hoopstreet/TikTok-Prompt-Generator
- **Docker Hub:** https://hub.docker.com/r/hoopstreet/tiktok-prompt-generator
- **Hugging Face:** https://huggingface.co/spaces/hoopstreet/TikTok-Prompt-Generator

## 🏗 Project Structure & Setup
1. **Local Repository (iSH/iPhone):**
   - `hf_moondream.py`: Core vision logic for TikTok prompt generation.
   - `Dockerfile`: Instructions for the Docker image (pulled by HF).
   - `deploy.sh`: Automation script for DNS, tagging, and pushing.
   - `.github/workflows/docker-publish.yml`: CI/CD pipeline logic.
   - `.env`: Local environment variables (not pushed to GitHub).

2. **Source Control (GitHub):**
   - **Main Branch**: Holds the current stable code.
   - **Tags (v1.x.x)**: Triggers the Docker Hub build.
   - **Secrets**: Stores `DOCKERHUB_TOKEN`, `DOCKERHUB_USERNAME`, and `HF_TOKEN`.

3. **Image Registry (Docker Hub):**
   - Stores the built image layers (Torch, Transformers, Moondream weights).
   - Provides the "Pre-built" image to Hugging Face to bypass long build times.

4. **Production (Hugging Face Spaces):**
   - **Hardware**: T4 Small (Free GPU tier).
   - **Deployment**: Pulls from Docker Hub using the versioned tag.
   - **Interface**: Gradio/Streamlit UI for generating prompts from images/videos.

## ⚙️ Initial Setup Guide
1. Initialize local Git: `git init`
2. Set remote: `git remote add origin https://github.com/hoopstreet/TikTok-Prompt-Generator.git`
3. Create deployer: `chmod +x deploy.sh`
4. First Push: `./deploy.sh v1.0.0`

## 🛠 Project Tools
1. **iSH iPhone**: Control Center for Git and versioning.
2. **GitHub**: Source code hosting and Automation engine.
3. **Docker Hub**: Versioned image registry.
4. **Hugging Face**: GPU-accelerated deployment space.

## 🤖 Dual-Action Workflow
1. **Build & Push**: Triggered by tag (v*). Builds image and pushes to Docker Hub.
2. **Sync HF**: Triggered by tag. Updates 'hf.Dockerfile' with the new tag and pushes to Hugging Face Space.

## 🏷 Version Expansion (v1.x.x)
- Tagging v1.x.x creates a matching name in Docker Hub.
- GitHub Actions automatically edits 'hf.Dockerfile' to point to the new Docker Hub tag.

## 🧠 AI Developer Logic: The Deployment Engine
### The "Push-to-GPU" Chain
1. **Local (iSH)**: User runs `./deploy.sh v1.x.x`.
   - **Logic**: Fixes DNS -> Updates local 'hf.Dockerfile' text -> Commits -> Pushes Tag.
2. **Cloud (GitHub Actions)**: Detects the new Tag.
   - **Job A (DockerHub)**: Builds the heavy Python environment + Moondream 3 weights.
   - **Job B (Hugging Face)**: Auto-edits the 'hf.Dockerfile' in the cloud to match the new Tag, then force-pushes to the Hugging Face Space.
3. **Execution (Hugging Face)**: Sees the new 'Dockerfile' -> Pulls the pre-baked image from DockerHub -> Starts the GPU server in seconds.

### Why this structure?
- **Speed**: We never build on Hugging Face (too slow). We build on GitHub.
- **Persistence**: iSH is the "Remote Control." GitHub is the "Factory." HF is the "Storefront."

## 🧱 Source Code Structure
1. **hf_moondream.py**: The entry point. Contains the Gradio UI and Moondream 3 inference logic.
2. **hf.Dockerfile**: The production Dockerfile used by Hugging Face to pull the pre-built image.
3. **Dockerfile**: The build-instruction file used by GitHub Actions to create the Docker Hub image.
4. **deploy.sh**: The local master script for versioning and pushing from iSH.
5. **.github/workflows/**: Contains 'docker-publish.yml' (Build) and 'hf-sync.yml' (Deploy).

## 🔢 Step-by-Step AI Setup
1. **Sync**: iSH pushes code to GitHub main branch.
2. **Tag**: iSH pushes version tag (e.g., v1.0.4).
3. **Build**: GitHub Actions builds the Moondream environment and pushes to Docker Hub.
4. **Link**: GitHub Actions updates the 'FROM' line in 'hf.Dockerfile' to match the new tag.
5. **Reboot**: Hugging Face detects the 'hf.Dockerfile' change and pulls the fresh image.

## 🛠 Tools & Ecosystem
1. **iSH iPhone**: Mobile Control Center (Git, versioning, DNS fixes).
2. **GitHub**: Automation Hub (Source code & Actions).
3. **Docker Hub**: Registry for versioned pre-built images.
4. **Hugging Face**: GPU Deployment Space (Free T4 tier).

## 🤖 Dual GitHub Actions Workflow
- **Workflow 1 (Build)**: Triggered by tags (v*). Builds the Docker image and pushes it to Docker Hub as 'v1.x.x'.
- **Workflow 2 (Sync)**: Triggered by tags. Automatically edits 'hf.Dockerfile' to match the new tag and pushes ONLY 'hf.Dockerfile' and 'README.md' to Hugging Face.

## 🏷 Version Expansion (v1.x.x)
Pushing a tag (e.g., v1.0.4) triggers the 'Expansion' logic:
GitHub Actions -> Edits 'FROM hoopstreet/tiktok-prompt-generator:v1.0.4' in 'hf.Dockerfile' -> Pushes to HF Space -> HF pulls the pre-built image.

## 🧬 Expansion Logic: The Auto-Editor
When you push a tag (v1.x.x) from iSH, the Cloud Factory performs these steps:
1. **Target**: Identifies the latest 'hf.Dockerfile' in the main branch.
2. **Edit**: Replaces the 'FROM' version tag to match the new GitHub Tag.
3. **Deploy**: Pushes the modified Dockerfile and README.md to Hugging Face.
4. **Result**: Hugging Face instantly reboots and pulls the pre-baked image.

## 🤖 AI Developer Protocol (For LLMs)
1. **No Manual Edits**: Never ask the user to manually edit files via 'vi' or 'nano'.
2. **Automated Input**: Always provide code using 'cat <<EOF >' or 'sed' for easy copy-pasting into iSH.
3. **Connectivity First**: Always include 'echo "nameserver 8.8.8.8" > /etc/resolv.conf' in the first line of Git operations.
4. **Scannability**: Break long scripts into numbered parts (1, 2, 3) to prevent clipboard issues in iSH.
5. **Contextual Sync**: Always end a logic update with a Git commit and push to maintain the 'Remote Control' status of the iPhone.

## 🏗 Source Code Structure (Logic Map)
- **hf_moondream.py**: Core AI Brain (Gradio UI + Moondream 3).
- **hf.Dockerfile**: The "Expansion" link (Points to Docker Hub).
- **Dockerfile**: The "Factory" instructions (Builds the environment).
- **.github/workflows/**: The "Cloud Hands" (Automates the deployment).
