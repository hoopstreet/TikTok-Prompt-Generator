# TikTok-Prompt-Generator DNA 🧬

## 🚀 1. The Architecture (Weightless Deployment)

This project is designed for "Zero-Local-Load" development.

| Component | Role | Description |
|-----------|------|-------------|
| iSH iPhone | Commander | Local terminal for coding |
| GitHub Actions | Builder | CI/CD pipeline |
| Docker Hub | Warehouse | Stores pre-baked images |
| Hugging Face Space | Live App | Runs Gradio UI on T4 GPU |
| HF Model Hub | Weights | Stores Moondream 3 (18GB+) |

---

## 🛠 2. Tool Purposes & Tech Stack

| Tool | Purpose | Tech Specs |
|------|---------|-------------|
| iSH (iPhone) | Local terminal | Alpine Linux |
| GitHub | Version control | Git |
| GitHub Actions | CI/CD | YAML Workflows |
| Docker Hub | Registry | Docker Registry |
| HF Space | Hosting | T4 GPU (16GB) |
| Moondream 3 | VLM | 9B Parameters |
| Gradio | UI | Python |
| Supabase | Database | PostgreSQL |

---

## 🔗 3. Project Links

- GitHub: https://github.com/hoopstreet/TikTok-Prompt-Generator
- Docker Hub: https://hub.docker.com/r/hoopstreet/tiktok-prompt-generator
- HF Space: https://huggingface.co/spaces/hoopstreet/TikTok-Prompt-Generator
- HF Model: https://huggingface.co/hoopstreet/moondream3-preview


## 🔐 4. Variables & Secrets (GitHub Settings)

| Secret Name | Purpose | Required |
|-------------|---------|----------|
| DOCKERHUB_USERNAME | Docker Hub account | YES |
| DOCKERHUB_TOKEN | Docker Hub token | YES |
| HF_TOKEN | Hugging Face token | YES |
| SUPABASE_URL | Database URL | OPTIONAL |
| SUPABASE_SERVICE_ROLE_KEY | Supabase key | OPTIONAL |

---

## 🤖 5. Dual-Action Workflow (GitHub Actions)

### Workflow 1: Build & Push (docker-publish.yml)
- Trigger: Push tag (v*)
- Action: Builds Docker image
- Output: hoopstreet/tiktok-prompt-generator:vX.X.X

### Workflow 2: Sync & Update HF (hf-sync.yml)
- Trigger: Success of Workflow 1
- Action: Updates hf.Dockerfile
- Output: HF Space rebuilds


## 🧠 6. AI Training Core Integration

### Input Fields (Matched with app.py)

| Field Name | Type | Description |
|------------|------|-------------|
| product_title | Text | Name of the product |
| about_this_product | Text | Short description |
| product_description | Text | Detailed description |
| image_url | Text | TikTok Shop image URL |

### Output Fields (Database Column Mapping)

| Column | Format | Description |
|--------|--------|-------------|
| positive_prompt | Shot-by-shot visual + dialogue | Video prompt |
| negative_prompt | Quality exclusion list | Anti-glitch |
| final_title | SEO title + 5 hashtags | TikTok-ready |

---

## 📦 7. Current Version: v1.6.0

### Features Implemented

- 4-Card Output Protocol
- Taglish Localization (8+ phrases)
- Niche Detection (10+ categories)
- Image URL Analyzer (ByteDance CDN)
- Shot-Based Script Generation
- Database Column Mapping
- Mobile-Safe Code Delivery


## ⌨️ 8. AI Developer Protocol (STRICT MODE)

### Rule 1: DNS FIRST
echo "nameserver 8.8.8.8" > /etc/resolv.conf

### Rule 2: NO MANUAL EDITS
- Never ask user to open nano/vi
- Fully automated script-based updates only

### Rule 3: HARD LENGTH LIMIT
- Blocks >150 chars WITHOUT split = INVALID
- MUST split into multiple cat EOF parts

### Rule 4: EOF SAFETY
- Start: cat << 'EOF' > file
- End: EOF
- Never nest cat inside cat

### Rule 5: MOBILE-FIRST
- Assume iPhone iSH environment
- Break long strings into multiple lines


## 📌 9. Version History

### v1.6.0 (2026-04-19) - STABLE
- 4-card output protocol
- Full AI_TRAINING_CORE.md integration
- Matched input fields
- Database column mapping

### v1.4.1 (2026-04-19) - STABLE
- Mobile-safe code delivery
- 150-char fragmentation rule
- EOF safety enforcement

### v1.3.3 (2026-04-19) - STABLE
- Fixed Dockerfile
- Weightless deployment confirmed

---

## 🔄 10. Deployment Flow

iSH Mobile (git tag v1.6.0)
    ↓
GitHub Actions (docker-publish.yml)
    ↓
Docker Hub (image:v1.6.0)
    ↓
GitHub Actions (hf-sync.yml)
    ↓
Hugging Face Space (pulls image)
    ↓
Model loaded from HF Model Hub at runtime

---

**DNA-Signature: HOOPSTREET-AFFILIATE-LOGIC-2026**
**Version: v1.6.0**

