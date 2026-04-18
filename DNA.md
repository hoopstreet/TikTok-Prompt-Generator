# TikTok-Prompt-Generator DNA 🧬

## 🚀 1. The Architecture (Weightless Deployment)
This project uses a "Remote-Control" architecture. We use low-power mobile hardware to trigger high-power cloud infrastructure.

* **Control Center (iSH iPhone):** The "Brain" where code is written and version tags are issued.
* **The Factory (GitHub Actions):** The "Muscle" that builds heavy Docker images.
* **The Registry (Docker Hub):** The "Storage" for pre-built versioned environments.
* **The Storefront (Hugging Face):** The "Stage" where the AI runs on a T4 GPU.

## 🛠 2. Tech Stack & Tools
* **Vision Model:** Moondream 3 (9B Parameters).
* **Runtime:** Python 3.10-slim.
* **iSH (Alpine Linux):** Local Git, DNS management, and versioning.
* **GitHub Actions:** Dual-workflow automation engine.
* **Hugging Face Spaces:** Production environment (GPU enabled).

## 🤖 3. Dual-Action Workflow (Expansion Logic)
When a version tag (`v1.x.x`) is pushed from iSH, two automated jobs trigger:

### Workflow A: Build & Push
* **Trigger:** New Tag (`v*`).
* **Process:** GitHub builds the full Docker environment including model weights.
* **Output:** A tagged image in Docker Hub (e.g., `hoopstreet/tiktok-prompt-generator:v1.0.4`).

### Workflow B: Sync & Deploy (The Auto-Editor)
* **Trigger:** Success of Workflow A.
* **Process:** 1. GitHub automatically edits `hf.Dockerfile`.
    2. It updates the `FROM` line to match the new version tag.
    3. It force-pushes ONLY `hf.Dockerfile` and `README.md` to Hugging Face.
* **Result:** Hugging Face pulls the new pre-built image instantly.

## 🧱 4. Source Code Logic Map
* **hf_moondream.py:** Core AI entry point (Gradio UI + Inference logic).
* **Dockerfile:** Build instructions for the "Factory" (Docker Hub).
* **hf.Dockerfile:** The "Expansion" link used by Hugging Face (Lightweight).
* **deploy.sh:** Local master script for tagging and pushing.
* **.github/workflows/:** Contains `docker-publish.yml` and `hf-sync.yml`.

## 🤖 5. AI Developer Protocol (For AI/LLMs)
To maintain the integrity of this mobile-first environment, all AI providers must follow these rules:
1.  **Keyboard-less Input:** Use `cat <<EOF >` or `sed` for all code. Never ask for manual edits.
2.  **DNS Resilience:** Always include `echo "nameserver 8.8.8.8" > /etc/resolv.conf` in Git operations.
3.  **Step-by-Step Blocks:** Break code longer than 200 characters into numbered segments (1, 2, 3).
4.  **Automatic Sync:** Always end a logic update with a Git commit and push.
5.  **No Overwriting:** Insert or append code into target places instead of rewriting the entire project.

## 📌 6. Version History
* **v1.0.0 - v1.0.2:** Infrastructure setup and refactoring.
* **v1.0.3:** [STABLE] Fixed Dockerfile renaming and iSH-to-GitHub pipeline.
* **v1.0.4:** [CURRENT] Implemented AI Protocol and organized DNA structure.
