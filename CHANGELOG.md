# Changelog

## [v1.3.3] - 2026-04-19

### 🐛 Fixed
- Dockerfile: Replaced missing  with  and 
- Build error: Package not found in Debian Trixie repository resolved

### ✅ Architecture Verified
- GitHub → Docker Hub → Hugging Face Space pipeline confirmed
- Weightless deployment: No model weights in GitHub or Docker Hub
- Model loaded at runtime from 
- Free T4 GPU compatible with FP8 quantization

### 📦 Release Components
- GitHub: Code only (~200KB)
- Docker Hub: Prebuilt image 
- HF Space: Dockerfile only pulling from Docker Hub
- HF Model Hub: Weights only at 

---

## [v1.3.2] - 2026-04-19

### 🚀 Added
- Weightless deployment architecture finalised
- DNA.md documentation updated with architecture rules

### 🔧 Changed
- HF Space now uses only Dockerfile pulling from Docker Hub
- Model loading moved to runtime from HF Model Hub

---

## [v1.3.1] - 2026-04-18

### 🔧 Changed
- Infrastructure stability improvements
- Tagging workflow validated

---

## [v1.3.0] - 2026-04-18

### 🚀 Added
- Weightless deployment preparation
- GitHub Actions dual-workflow configuration

---

## [v1.2.4] - 2026-04-18

### 🐛 Fixed
- HF offline mode enforced
- Local Moondream inference only

---

## [v1.2.3] - 2026-04-18

### 🐛 Fixed
- HF crash hotfix
- Removed remote model download dependency

---

## [v1.2.0] - 2026-04-18

### 🔧 Changed
- Architecture shift to local inference
- Removed HF model dependency at runtime

---

## [v1.1.8] - 2026-04-18

### 🚀 Added
- Transition bridge to v1.2.0 logic
- DNA.md manifest completeness

---

## [v1.1.7] - 2026-04-18

### 🤖 AI Summary
- Auto-generated release notes
- Pipeline stability verified

---

## [v1.1.6] - 2026-04-18

### 🚀 Added
- Batch deploy validation
- Multi-version tagging confirmed

---

## [v1.1.5] - 2026-04-18

### 🚀 Added
- Auto DNA logging introduced
- deploy.sh automation active

---

## [v1.1.4] - 2026-04-18

### 🔧 Fixed
- Master deployment fix
- Docker + Gradio integration corrected

---

## [v1.1.3] - 2026-04-18

### 🔧 Changed
- Absolute imports finalized
- Torch 2.5.1 enforced
- Infrastructure stabilized

---

## [v1.0.9] - 2026-04-17

### 🔧 Changed
- Weightless build finalised
- Strict version tagging
- Removed 'latest' bloat

---

## [v1.0.8] - 2026-04-17

### 🐛 Fixed
- Workflow syntax fix
- Literal EOF protection

---

## [v1.0.7] - 2026-04-17

### 🔧 Fixed
- Dual-Action Workflow (Main/Tag)
- Clean HF Sync logic

---

## [v1.0.6] - 2026-04-17

### 🚀 Added
- Taglish Video Script templates
- TikTok-specific prompt logic

---

## [v1.0.5] - 2026-04-17

### 🚀 Added
- TikTok-specific Taglish prompt logic preparation

---

## [v1.0.4] - 2026-04-17

### 🚀 Added
- Master DNA Overhaul
- AI Developer Protocol
- Secret Documentation

---

## [v1.0.3] - 2026-04-16

### 🔧 Fixed
- Infrastructure fixes
- DNS stability

---

## [v1.0.2] - 2026-04-16

### 🔧 Fixed
- DNS and network improvements

---

## [v1.0.1] - 2026-04-16

### 🚀 Added
- Initial infrastructure setup

---

## [v1.0.0] - 2026-04-16

### 🚀 Added
- Initial release
- Moondream 3 integration
- Gradio UI base
