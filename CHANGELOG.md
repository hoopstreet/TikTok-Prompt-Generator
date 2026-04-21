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
