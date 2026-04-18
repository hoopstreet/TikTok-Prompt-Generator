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
