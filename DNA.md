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
