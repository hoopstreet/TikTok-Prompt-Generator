# Changelog
## [v4.0.2] - 2026-04-21
### Added
- Vite frontend + FastAPI backend architecture.
- Full AI_TRAINING_CORE compliance check workflow.
- 11 Niche categories (Beauty, Tech, Sports, etc.).
- Taglish localization with 10+ phrases.
### Fixed
- Multi-stage Docker build fragmentation.


## [v4.1.0] - $(date '+%Y-%m-%d')

### Added
- AI Code Analyzer workflow (scans repo every 6 hours)
- AI Auto Fix workflow (PR-based fixes)
- AI Test Runner (validation gate)
- AI Auto Merge (safe merge with test gating)
- AI Version Bump (automatic versioning)
- AI Training Sync (aligns with AI_TRAINING_CORE)
- AI Self-Healing Loop (complete automation)

### Changed
- Separated monolithic workflow into 7 focused workflows
- Integrated DeepSeek API for real AI code generation
- PR-based fixes instead of direct commits

### Fixed
- Auto-merge now requires test approval
- Added proper error handling
- Mobile-safe code formatting

### Security
- AI cannot push directly to main
- All changes require PR review
- Test gating enforced before merge


## [v4.2.1] - $(date '+%Y-%m-%d') - CURRENT

### Added
- DeepSeek via Hugging Face (fallback when API key missing)
- 5-model fallback chain (DeepSeek API → DeepSeek HF → CodeLlama → StarCoder → CodeGen)
- Credential flexibility - works with API key OR HF token OR both
- Enhanced status reporting with model availability

### Changed
- Multi-model AI now supports DeepSeek through two providers
- Improved fallback logic for better reliability
- Updated documentation with credential options

### Models Available (5 total)
1. DeepSeek Coder (API) - Best quality, requires API key
2. DeepSeek Coder (Hugging Face) - Same model, uses HF token
3. CodeLlama 7B - Free via Hugging Face
4. StarCoder2 3B - Free via Hugging Face
5. CodeGen 350M - Free via Hugging Face

### Configuration Options
- **Option A**: Add DEEPSEEK_API_KEY → Get best quality
- **Option B**: Add HF_TOKEN → Get 4 free models including DeepSeek
- **Option C**: Both → Maximum coverage and fallbacks
- **Option D**: None → Rule-based fallback (basic functionality)

