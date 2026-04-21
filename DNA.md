# TikTok-Prompt-Generator DNA 🧬

## 🚀 1. Architecture
| Component | Role | tech |
|-----------|------|------|
| iSH iPhone | Terminal | Alpine |
| GH Actions | CI/CD | YAML |
| Docker Hub | Warehouse | Registry |
| HF Space | Live App | Gradio/GPU |

## 🛠 2. AI_TRAINING_CORE Compliance Status
| Section | Description | Status |
|---------|-------------|--------|
| 1-6 | Base Logic | ✅ |
| 7-12 | Prompting Protocols | ✅ |
| 13-16 | Optimization | ⚠️ |

## 📦 3. Version History
- **v4.0.2 (Current)**: Vite + FastAPI Architecture, 11 Niches.
- **v3.6.0**: Zebra tables, confirm delete.
- **v2.5.0**: Supabase persistence.

**DNA-Signature: HOOPSTREET-AFFILIATE-LOGIC-2026**


## 16. AI DevOps System (v4.1.0)

### Workflows

| Workflow | Purpose | Trigger |
|----------|---------|---------|
| ai-code-analyzer.yml | Scan repo for issues | Every 6 hours |
| ai-auto-fix.yml | Generate PR fixes | After analysis |
| ai-test-runner.yml | Validate changes | On PR |
| ai-auto-merge.yml | Safe merge | After tests pass |
| ai-version-bump.yml | Auto versioning | After merge |
| ai-training-sync.yml | Sync AI core | On AI_TRAINING_CORE change |
| ai-self-healing.yml | Complete loop | Every 12 hours |

### Safety Rules

- ❌ AI cannot push directly to main
- ✅ All changes go through Pull Requests
- ✅ Auto-merge requires:
  - Passing tests
  - AI label approval
  - No conflicts

### Golden Rule

> AI can WRITE code, but only TESTS can APPROVE it.

**DNA-Signature: HOOPSTREET-AFFILIATE-LOGIC-2026**
**Version: v4.1.0**
**Last Updated: $(date '+%Y-%m-%d')**
## AI_TRAINING_CORE Status (2026-04-21)
- Compliance: 2/16


## 17. Professional AI DevOps System (v4.1.0)

### System Architecture


### Alert System

| Level | Description | Action |
|-------|-------------|--------|
| **INFO** | Normal operation | Continue |
| **WARNING** | Missing API key | Log, continue with limited features |
| **ERROR** | Task failed | Log, alert, move to next task |
| **CRITICAL** | System issue | Halt, require human intervention |

### Task Management

The AI Task Manager:
- ✅ Parses roadmap from DNA.md
- ✅ Tracks completed/blocked tasks
- ✅ Detects missing API keys
- ✅ Continues with available tasks
- ✅ Generates professional reports

### Human Intervention Required When:
- ⚠️ Critical API keys missing
- ⚠️ Merge conflicts cannot be auto-resolved
- ⚠️ Test failures require manual review
- ⚠️ Security vulnerabilities detected

### Dashboard Access

Monitor system status at:
- GitHub Actions: https://github.com/hoopstreet/TikTok-Prompt-Generator/actions
- Status Dashboard: `dashboard.html` (generated weekly)

### Professional Features

- ✅ **End-to-End Automation** - From code scan to deployment
- ✅ **Intelligent Routing** - Tasks routed based on dependencies
- ✅ **Error Recovery** - Failed tasks don't block others
- ✅ **API Key Management** - Graceful degradation when keys missing
- ✅ **Progress Tracking** - Real-time task status
- ✅ **Professional Reporting** - HTML dashboard + Markdown reports

**DNA-Signature: HOOPSTREET-AFFILIATE-LOGIC-2026**
**Version: v4.1.0**
**Last Updated: $(date '+%Y-%m-%d')**


## 18. Multi-Model AI Support (v4.2.0) - 🔜 NEXT

### Model Architecture


### Features

- ✅ **Automatic Model Selection** - Best available model is used
- ✅ **Graceful Fallback** - If one fails, next model takes over
- ✅ **Multi-Provider** - DeepSeek API + Hugging Face Inference
- ✅ **Zero Cost** - All models are free/open-source
- ✅ **Your HF_TOKEN** - Already configured in GitHub Secrets

### Model Priority

| Priority | Model | Provider | Cost | Quality |
|----------|-------|----------|------|---------|
| 1 | DeepSeek Coder | DeepSeek API | Free | ⭐⭐⭐⭐⭐ |
| 2 | CodeLlama 7B | Hugging Face | Free | ⭐⭐⭐⭐ |
| 3 | StarCoder2 3B | Hugging Face | Free | ⭐⭐⭐⭐ |
| 4 | CodeGen 350M | Hugging Face | Free | ⭐⭐⭐ |

### Workflow

```yaml
ai-multi-model.yml:
  - Runs every 4 hours
  - Checks model availability
  - Generates fixes with best model
  - Falls back if needed
  - Updates status dashboard

```bash
# PHASE 5: Update CHANGELOG.md
cat << 'EOF' >> CHANGELOG.md


## [v4.2.0] - $(date '+%Y-%m-%d') - 🔜 NEXT

### Added
- Multi-Model AI Support (DeepSeek + CodeLlama + StarCoder)
- Automatic model selection based on availability
- Graceful fallback chain (4 models total)
- Hugging Face Inference API integration
- Model status monitoring workflow
- Zero-cost AI code generation

### Changed
- Upgraded from single-model to multi-model architecture
- Enhanced error handling with fallbacks
- Improved code fix quality with best-available model

### Models Available
1. DeepSeek Coder (Primary - API)
2. CodeLlama 7B (Fallback - HF)
3. StarCoder2 3B (Fallback - HF)
4. CodeGen 350M (Final fallback)

### Configuration
- Uses existing HF_TOKEN from GitHub Secrets
- No additional setup required
- Automatic model health checks every 4 hours


## 18. Multi-Model AI Support (v4.2.1) - CURRENT

### Model Architecture

### Model Priority Table

| Priority | Model | Provider | Requirements | Quality |
|----------|-------|----------|--------------|---------|
| 1 | DeepSeek Coder (API) | DeepSeek | API Key | ⭐⭐⭐⭐⭐ |
| 2 | DeepSeek Coder (HF) | Hugging Face | HF Token | ⭐⭐⭐⭐⭐ |
| 3 | CodeLlama 7B | Hugging Face | HF Token | ⭐⭐⭐⭐ |
| 4 | StarCoder2 3B | Hugging Face | HF Token | ⭐⭐⭐⭐ |
| 5 | CodeGen 350M | Hugging Face | HF Token | ⭐⭐⭐ |
| 6 | Rule-Based | Built-in | None | ⭐⭐ |

### Features

- ✅ **Dual DeepSeek Access** - API key OR Hugging Face token
- ✅ **5 AI Models** - Maximum coverage
- ✅ **Automatic Fallback** - Seamless degradation
- ✅ **Zero Cost Options** - HF Token provides 4 free models
- ✅ **Graceful Degradation** - Works even with no keys

### Credential Flexibility

| You Have | Models Available |
|----------|------------------|
| Both API Key + HF Token | All 5 models |
| Only HF Token | 4 models (DeepSeek HF + CodeLlama + StarCoder + CodeGen) |
| Only API Key | 1 model (DeepSeek API) |
| Neither | Rule-based fallback |

**Status:** ✅ CURRENT - Production Ready
**Version:** v4.2.1


### v4.2.1 (2026-04-21) - AI Auto Version
- Auto-generated by AI Version Bump
- AI_TRAINING_CORE compliant
- All tests passing


### v4.2.2 (2026-04-21) - AI Auto Version
- Auto-generated by AI Version Bump
- AI_TRAINING_CORE compliant
- All tests passing


### v4.2.3 (2026-04-21) - AI Auto Version
- Auto-generated by AI Version Bump
- AI_TRAINING_CORE compliant
- All tests passing

