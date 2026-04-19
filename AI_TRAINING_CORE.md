# TikTok Affiliate AI Training Core
## Philippines Market - Moondream 3 Integration

### Version: v2.5.0
### DNA-Signature: HOOPSTREET-AFFILIATE-LOGIC-2026
### Region: PH-LOCALIZED

---

## 1. Visual Density & Pacing (3-Second Rule)

| Duration | Shots | Time per Shot |
|----------|-------|---------------|
| 15 seconds | Exactly 5 shots | 3 seconds |
| 30 seconds | Exactly 10 shots | 3 seconds |
| 45 seconds | Exactly 15 shots | 3 seconds |
| 55 seconds | Exactly 18 shots | 3 seconds |
| 60 seconds | Exactly 20 shots | 3 seconds |

RULE: No exceptions. Every shot = 3 seconds exactly.

---

## 2. Universal Niche Framework

| Niche | Focus Points |
|-------|--------------|
| Apparel | Fabric texture, stretch tests |
| Tech/Gadgets | Unboxing, POV usage |
| Home/Kitchen | Satisfying usage |
| Beauty | Real skin results |
| Mobile Accessories | Efficiency, safety |
| Motor/Car | Pogi points, upgrade |
| Audio | Crystal clear, bass-heavy |
| Gaming | No lag, RGB setup |
| Sports | Full sublimation, custom IGN, sulit-tela |
| Tools | Heavy-duty, rechargeable, handy |


## 3. Localization: Taglish Protocol

### Key Phrases (EN → TL)

| English | Taglish |
|---------|---------|
| It's so beautiful | Grabe ang ganda |
| Great quality | Solid ang quality |
| Very worth it | Sulit na sulit |
| Get yours now | Kunin niyo na yung sa'yo |
| You need this | Kailangan niyo to |
| Trust me | Swerte niyo |
| Amazing | Panalo |
| Cheap but quality | Mura pero quality |

### FORBIDDEN PATTERNS:
- No store names
- No formal Tagalog (po/opo)
- No English-only scripts

---

## 4. Multi-Card Output Protocol (4 Cards)

### Card 1: Product Info Card
[PRODUCT INFO CARD]
Product Name: [Name]
Category: [NICHE]
Key Features: [Features]

### Card 2: Video Brief Card
[VIDEO BRIEF CARD]
Niche: [niche]
Duration: [15/30/45] seconds
Shot Count: [5/10/15] shots


### Card 3: Video Analysis Results
[VIDEO ANALYSIS RESULTS]
Total Shots: [number]
Audio Style: Taglish voiceover
Resolution: 4K Vertical 9:16
Infinity Loop: Enabled - video auto-replays seamlessly

### Card 4: Video Storyboard Card
[VIDEO STORYBOARD CARD]
Shot 01 (3.0s): [Movement] [Lighting] + Dialogue
Shot 02 (3.0s): [Movement] [Lighting] + Dialogue

---

## 5. Database Column Mapping

Column: positive_prompt
Shot 01 (3s): 4K vertical 9:16 [Movement] + Dialogue

Column: negative_prompt
low quality, blurry, distorted, glitch, watermark

Column: final_title

### Shot Matching Rule:
- Each positive_prompt shot MUST have matching negative_prompt shot
- 1-to-1 Mapping: 5 positive shots = 5 negative shots
- Movement-specific anti-glitch keywords per shot
🔥 MUST-HAVE! [Product] #Hashtag1 #Hashtag2 #Hashtag3


## 6. Niche Keyword Library

### Apparel
Keywords: breathable, oversized, presko, aesthetic
Forbidden: fast-charging, heavy-duty

### Audio
Keywords: noise cancellation, bass-heavy, wireless
Forbidden: stretchable, breathable

### Gaming
Keywords: mechanical, RGB, zero delay, anti-ghosting
Forbidden: cozy, daily wear

### Tech/Powerbank
Keywords: PD fast charge, compact, LED indicator
Forbidden: stretch test, double-lined

### Motor/Car

### Sports/Jerseys
Keywords: moisture wicking, customized name, durable print, full sublimation
Forbidden: fast-charging, RGB, noise cancellation

### Tools/Hardware
Keywords: cordless, high torque, multi-bit, compact storage, LED work light
Forbidden: oversized fit, breathable, aesthetic decor
Keywords: upgradable, porma, DIY installation
Forbidden: soft fabric, aesthetic decor

---

## 7. Anti-Repetition Rules

- Review last 3 interactions
- Do NOT reuse same hook
- If previous was 15s → suggest 30s
- If user requested "More Tagalog" → increase density


## 8. Video Engine Directives

### Camera Movements:
- Cinematic Pan
- Dynamic Zoom-in
- Handheld POV shake
- Slow-motion reveal

### Lighting Keywords:
- Soft Studio Lighting
- Natural Sunlight
- Neon Glow

### Shot Framing:
- Close-up (CU)
- Medium Shot (MS)
- Macro Shot

---

## 9. SEO Title Optimization

| Parameter | Requirement |
|-----------|-------------|
| Length | 80-100 characters |
| Structure | Hook + Benefit + Urgency |
| Hashtags | Exactly 5 |
| Length Enforcement | 80-100 characters strict |

Valid Example:
🔥 MUST-HAVE! Grabe ang quality nito | Product #BudolFinds

---

## 10. Validation Checklist

- Duration matches shot count (3s each)
- Exactly 4 cards generated
- Taglish dialogue used
- No niche leakage
- Title 80-100 chars with 5 hashtags
- No store names mentioned


# PHASE 6: APPEND SHOT MATCHING DETAILS TO AI TRAINING CORE
cat << 'EOF' >> AI_TRAINING_CORE.md
# PHASE 6: APPEND SHOT MATCHING DETAILS TO AI TRAINING CORE
cat << 'EOF' >> AI_TRAINING_CORE.md

---

## 11. Shot Matching Rule (1-to-1 Mapping)

### Rule Description:
For every positive_prompt shot, there MUST be a corresponding negative_prompt shot.

### Example 5-Shot Mapping:
| Positive Shot | Negative Shot |
|---------------|---------------|
| Shot 01: Cinematic Pan | Shot 01 Negative: + no motion blur, no frame tearing |
| Shot 02: Dynamic Zoom | Shot 02 Negative: + no pixelation, no quality loss |
| Shot 03: Handheld POV | Shot 03 Negative: + no excessive shake, stable |
| Shot 04: Slow-motion | Shot 04 Negative: + no frame skipping, fluid motion |
| Shot 05: Cinematic Pan | Shot 05 Negative: + smooth transition |

### Movement-Specific Anti-Glitch Keywords:

| Camera Movement | Anti-Glitch Keywords |
|----------------|---------------------|
| Cinematic Pan | no motion blur, no frame tearing, smooth transition |
| Dynamic Zoom-in | no pixelation, no quality loss, sharp focus |
| Handheld POV | no excessive shake, no disorientation, stable |
| Slow-motion reveal | no frame skipping, no ghosting, fluid motion |

### Continuity Lock Keywords (All Shots):
- do not change logo position
- do not alter fabric color
- maintain product orientation
- consistent lighting throughout
- no object morphing


---

## 12. Supabase Database Integration

### Connection Configuration (supabase_connection.py)
- Singleton pattern for single connection instance
- Environment variables: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
- Automatic table existence checking

### Data Flow:
```

User Input → app.py → supabase_connection.py → Supabase Cloud
↓
generation_history (save all prompts)
training_materials (AI behavior rules)
chat_history (conversation memory)
testing_explorer (test results)

```

### Table Schemas Location:
- `supabase_schema.sql` - Main tables (generation_history, training_materials, chat_history)
- `supabase_testing_explorer.sql` - Testing table
- `supabase_rls_public.sql` - Row Level Security policies


---

## 13. Infinity Loop Directive

### Video Auto-Replay Feature:
- Videos automatically replay from start to end seamlessly
- Creates never-ending video effect for better engagement
- Implemented in Card 3: Video Analysis Results

### Implementation:
```

Infinity Loop: Enabled - video auto-replays seamlessly

```

### Technical Requirements:
- Smooth transition from last frame to first frame
- No visible jump or cut between replays
- Consistent audio synchronization
- Loop point should be natural (end of call-to-action)


---

## 14. Final Title Generation Rules (Strict 80-100 chars)

### Title Structure:
```

[Emoji] [Hook Emotion] + [Core Benefit] + [Urgency] | [Product Name] [5 Hashtags]

```

### Character Enforcement:
| Condition | Action |
|-----------|--------|
| >100 characters | Truncate product name by 5 chars |
| >100 characters again | Remove benefit phrase |
| <80 characters | Add "- Shop now!" suffix |
| Exactly 80-100 | ACCEPT |

### Valid Example (93 chars):
```

🔥 MUST-HAVE! Elite Athletic Shorts | APPAREL Finds #TikTokMadeMeBuyIt #BudolFinds #Sulit #Quality #Affiliate

```

### Hashtags (Always 5):
1. #TikTokMadeMeBuyIt
2. #BudolFinds
3. #Sulit
4. #Quality
5. #Affiliate (or niche-specific: #Athletic, #Gaming, #Audio)

