# TikTok-Prompt-Generator DNA 🧬

## 🚀 1. The Architecture (Weightless Deployment)

This project is designed for “Zero-Local-Load” development.

|Component         |Role     |Description               |
|------------------|---------|--------------------------|
|iSH iPhone        |Commander|Local terminal for coding |
|GitHub Actions    |Builder  |CI/CD pipeline            |
|Docker Hub        |Warehouse|Stores pre-baked images   |
|Hugging Face Space|Live App |Runs Gradio UI on T4 GPU  |
|HF Model Hub      |Weights  |Stores Moondream 3 (18GB+)|

-----

## 🛠 2. Tool Purposes & Tech Stack

|Tool          |Purpose        |Tech Specs     |
|--------------|---------------|---------------|
|iSH (iPhone)  |Local terminal |Alpine Linux   |
|GitHub        |Version control|Git            |
|GitHub Actions|CI/CD          |YAML Workflows |
|Docker Hub    |Registry       |Docker Registry|
|HF Space      |Hosting        |T4 GPU (16GB)  |
|Moondream 3   |VLM            |9B Parameters  |
|Gradio        |UI             |Python         |
|Supabase      |Database       |PostgreSQL     |

-----

## 🔗 3. Project Links

- GitHub: https://github.com/hoopstreet/TikTok-Prompt-Generator
- Docker Hub: https://hub.docker.com/r/hoopstreet/tiktok-prompt-generator
- HF Space: https://huggingface.co/spaces/hoopstreet/TikTok-Prompt-Generator
- HF Model: https://huggingface.co/hoopstreet/moondream3-preview

-----

## 🔐 4. Variables & Secrets (GitHub Settings)

|Secret Name              |Purpose           |Required|
|-------------------------|------------------|--------|
|DOCKERHUB_USERNAME       |Docker Hub account|YES     |
|DOCKERHUB_TOKEN          |Docker Hub token  |YES     |
|HF_TOKEN                 |Hugging Face token|YES     |
|SUPABASE_URL             |Database URL      |OPTIONAL|
|SUPABASE_SERVICE_ROLE_KEY|Supabase key      |OPTIONAL|

-----

## 🤖 5. Dual-Action Workflow (GitHub Actions)

### Workflow 1: Build & Push (docker-publish.yml)

- Trigger: Push tag (v*)
- Action: Builds Docker image
- Output: hoopstreet/tiktok-prompt-generator:vX.X.X

### Workflow 2: Sync & Update HF (hf-sync.yml)

- Trigger: Success of Workflow 1
- Action: Updates hf.Dockerfile
- Output: HF Space rebuilds

-----

## 🧠 6. AI Training Core Integration

### Input Fields (Matched with app.py)

|Field Name         |Type|Description          |
|-------------------|----|---------------------|
|product_title      |Text|Name of the product  |
|about_this_product |Text|Short description    |
|product_description|Text|Detailed description |
|image_url          |Text|TikTok Shop image URL|

### Output Fields (Database Column Mapping)

|Column         |Format                        |Description |
|---------------|------------------------------|------------|
|positive_prompt|Shot-by-shot visual + dialogue|Video prompt|
|negative_prompt|Quality exclusion list        |Anti-glitch |
|final_title    |SEO title + 5 hashtags        |TikTok-ready|

-----

## 📦 7. Current Version: v2.6.0

### Features Implemented

- 4-Card Output Protocol
- Taglish Localization (8+ phrases)
- Niche Detection (10+ categories)
- Image URL Analyzer (ByteDance CDN)
- Shot-Based Script Generation
- Database Column Mapping
- Mobile-Safe Code Delivery

-----

## 8. AI Developer Protocol (STRICT MODE)

### Rule 1: DNS FIRST

```sh
echo "nameserver 8.8.8.8" > /etc/resolv.conf
```

### Rule 2: NO MANUAL EDITS

- Never ask user to open nano/vi
- Fully automated script-based updates only

### Rule 3: HARD LENGTH LIMIT

- Blocks >150 chars WITHOUT split = INVALID
- MUST split into multiple cat EOF parts

### Rule 4: EOF SAFETY

```sh
# Start
cat << 'EOF' > file
EOF
# Never nest cat inside cat
```

### Rule 5: MOBILE-FIRST

- Assume iPhone iSH environment
- Break long strings into multiple lines

### Git Push Options

✅ OPTION 1 (SAFE — recommended) — Pull first, then push:

```sh
git pull origin main --rebase
git push origin main
```

Keeps remote commits, applies your changes on top, no history loss.

⚠️ OPTION 2 (FORCE PUSH — overwrite remote) — If you’re sure your version is correct:

```sh
git push origin main --force
```

Warning: overwrites remote history, can delete others’ commits.

-----

## 📌 9. Version History

### v2.6.0 (2026-04-19) - CURRENT

- 4-Card Output Protocol
- Full AI_TRAINING_CORE.md integration
- Matched input fields + database column mapping

### v2.5.0 (2026-04-19) - STABLE

- Full Supabase integration (4 tables)
- testing_explorer table for test results
- Singleton connection pattern
- Environment variables with .env.template
- Selectable history rows with export
- 55s duration (18 shots) added
- Sports and Tools niches added
- Infinity loop enabled
- Shot matching rule enforced

### v1.6.0 (2026-04-19) - STABLE

### v1.4.1 (2026-04-19) - STABLE

- Mobile-safe code delivery
- 150-char fragmentation rule
- EOF safety enforcement

### v1.3.3 (2026-04-19) - STABLE

- Fixed Dockerfile
- Weightless deployment confirmed

-----

## 🔄 10. Deployment Flow

```
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
    ↓
Supabase Cloud (generation_history, training_materials, chat_history, testing_explorer)
```

-----

## 📁 11. Complete File Structure Reference

```
TikTok-Prompt-Generator/
├── .github/workflows/
│   ├── docker-publish.yml      # Builds Docker image on tags
│   └── hf-sync.yml             # Syncs to Hugging Face Space
├── app.py                      # Main Gradio UI (7 Textboxes, 3 Buttons, 1 Dataframe)
├── Dockerfile                  # Docker build instructions (Python 3.10-slim)
├── hf.Dockerfile               # HF Space redirect (pulls from Docker Hub)
├── requirements.txt            # Python dependencies (torch, gradio, supabase, pandas)
├── supabase_connection.py      # Supabase singleton connection class
├── supabase_schema.sql         # Generation history, training materials, chat history tables
├── supabase_testing_explorer.sql  # Testing explorer table
├── supabase_rls_public.sql     # Row Level Security policies
├── AI_TRAINING_CORE.md         # Complete AI training manual (20 sections)
├── DNA.md                      # Master documentation (this file)
├── README.md                   # Public-facing documentation
├── LICENSE.md                  # MIT License
├── .env.template               # Environment variables template
├── .gitignore                  # Ignores .env, pycache, *.pyc
└── .gitattributes              # Git LFS configuration
```

-----

## 🔌 12. API Reference (Supabase Methods)

### Generation History Methods

|Method                    |Parameters                                |Returns|Description                 |
|--------------------------|------------------------------------------|-------|----------------------------|
|`save_generation()`       |input_field, analyst_product, final_output|Boolean|Stores generated prompt     |
|`get_generation_history()`|limit=100                                 |Array  |Retrieves recent generations|
|`delete_generation()`     |record_id                                 |Boolean|Deletes specific record     |

### Training Materials Methods

|Method                      |Parameters               |Returns|Description                      |
|----------------------------|-------------------------|-------|---------------------------------|
|`save_training_material()`  |topic, content           |Boolean|Adds AI behavior rule            |
|`get_training_materials()`  |topic=None               |Array  |Retrieves rules (filter by topic)|
|`update_training_material()`|record_id, topic, content|Boolean|Updates existing rule            |
|`delete_training_material()`|record_id                |Boolean|Deletes rule                     |

### Chat History Methods (Memory)

|Method                     |Parameters                                     |Returns|Description             |
|---------------------------|-----------------------------------------------|-------|------------------------|
|`save_chat_message()`      |conversation_id, user_input, ai_response, niche|Boolean|Stores conversation     |
|`get_chat_history()`       |conversation_id, limit=10                      |Array  |Retrieves conversation  |
|`get_last_n_messages()`    |conversation_id, n=3                           |Array  |Gets last N messages    |
|`delete_old_chat_history()`|days=30                                        |Boolean|Auto-cleanup old records|

### Testing Explorer Methods

|Method              |Parameters                                             |Returns|Description                 |
|--------------------|-------------------------------------------------------|-------|----------------------------|
|`save_test_result()`|test_name, test_input, test_output, status, duration_ms|Boolean|Stores test result          |
|`get_test_results()`|limit=50                                               |Array  |Retrieves test history      |
|`get_test_stats()`  |None                                                   |Dict   |Returns pass/fail statistics|

-----

## 📚 13. AI Training Materials Responsibility

### Supabase Backend Tables

|Table             |Purpose                     |Methods                  |
|------------------|----------------------------|-------------------------|
|generation_history|Stores all generated prompts|save, get, delete        |
|training_materials|AI behavior rules           |save, get, update, delete|
|chat_history      |Conversation memory         |save, get, delete old    |
|testing_explorer  |Test results tracking       |save, get, stats         |

### Supabase Connection Details (supabase_connection.py)

Singleton pattern for database connections:

```python
class SupabaseConnection:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

Environment Variables Required:

- `SUPABASE_URL` — Your Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY` — Service role key for API access

### Table Schema Files

|Table             |File Reference        |SQL File                     |
|------------------|----------------------|-----------------------------|
|generation_history|supabase_connection.py|supabase_schema.sql          |
|training_materials|supabase_connection.py|supabase_schema.sql          |
|chat_history      |supabase_connection.py|supabase_schema.sql          |
|testing_explorer  |supabase_connection.py|supabase_testing_explorer.sql|

### Data Flow

```
User Input → app.py → supabase_connection.py → Supabase Cloud
                                ↓
            generation_history  (save all prompts)
            training_materials  (AI behavior rules)
            chat_history        (conversation memory)
            testing_explorer    (test results)
```

### Auto-Cleanup

- A Supabase Edge Function deletes chat_history older than 30 days
- Prevents database bloat while maintaining context for Niche Isolation
- Runs via pg_cron every 24 hours

-----

## 📝 14. DNA Update Protocol

### Purpose of DNA.md

This file serves as the **master documentation** for:

- Project architecture and deployment
- Tool purposes and tech stack
- Environment variables and secrets
- CI/CD workflows
- Version history tracking
- File structure reference
- API documentation

### When to Update DNA.md

|Trigger            |Action                               |
|-------------------|-------------------------------------|
|New version tag    |Append to Version History (Section 9)|
|New file added     |Update File Structure (Section 11)   |
|New API method     |Update API Reference (Section 12)    |
|Architecture change|Update Deployment Flow (Section 10)  |
|New secret/variable|Update Variables (Section 4)         |

### Update Rules (STRICT)

1. **APPEND** new information — NEVER overwrite
1. **PRESERVE** existing documentation
1. **MAINTAIN** section numbering
1. **KEEP** DNA-Signature at bottom

-----

## 🤖 15. AI Auto-Update Instructions

### For Training Materials (AI_TRAINING_CORE.md)

When AI detects new requirements, append to appropriate section:

```bash
# Example: Adding new duration
sed -i '/| 60 seconds/a| 65 seconds | Exactly 22 shots | 3 seconds |' AI_TRAINING_CORE.md

# Example: Adding new niche
sed -i '/| Tools/a| NewNiche | Focus points |' AI_TRAINING_CORE.md

# Example: Adding new Taglish phrase
sed -i '/| Cheap but quality/a| New English | New Taglish |' AI_TRAINING_CORE.md
```

### For DNA.md

When new features are deployed, append version history:

```bash
# Example: Adding new version
sed -i '/### v2.6.0/a\
\
### v2.7.0 (YYYY-MM-DD) - STABLE\
- New feature description' DNA.md
```

### Verification After Update

Always verify with:

```bash
grep "^## [0-9]" AI_TRAINING_CORE.md | wc -l
grep "^## " DNA.md | wc -l
```

-----

**DNA-Signature: HOOPSTREET-AFFILIATE-LOGIC-2026**
**Version: v2.6.0**

### v4.0.0 (2026-04-21) - CURRENT
- Full AI_TRAINING_CORE.md implementation (Sections 1-16)
- HF Space deployment ready
- Gradio UI with 4-card output protocol
- Taglish localization with 10+ phrases
- Niche detection for 11 categories
- 1-to-1 positive/negative prompt mapping
- Random shot timings from 2.1s-5.0s pool
- 15-55s duration support
- SEO titles with 80-100 chars, 5 hashtags
- Infinity loop directive in Card 3
- Mobile-first design for iSH compatibility

