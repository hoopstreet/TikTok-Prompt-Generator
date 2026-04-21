from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
import random
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="TikTok Prompt Generator API", version="4.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase init
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
supabase = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client, Client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except:
        pass

class ProductInput(BaseModel):
    product_title: str
    about_this_product: str
    product_description: str
    image_url: Optional[str] = None

class GenerationResponse(BaseModel):
    id: str
    positive_prompt: str
    negative_prompt: str
    final_title: str
    cards: Dict[str, Any]
    created_at: str

class AITrainingCore:
    SHOT_TIMINGS = [2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9,
                    3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8,
                    3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7,
                    4.8, 4.9, 5.0]
    
    DURATIONS = {
        15: 5, 18: 6, 20: 7, 22: 7, 25: 8, 28: 9, 30: 10,
        32: 11, 35: 12, 38: 13, 40: 13, 42: 14, 45: 15,
        48: 16, 50: 17, 55: 18
    }
    
    NICHES = {
        "apparel": {"keywords": ["shirt","pants","hoodie","dress","fabric","shorts"],
                    "focus": ["Oversized Fit","Presko","breathable","aesthetic"],
                    "forbidden": ["fast-charging","heavy-duty","RGB"],
                    "hashtag": "#ApparelFinds"},
        "audio": {"keywords": ["earbuds","headphones","speaker","bass","wireless"],
                  "focus": ["Crystal Clear","Bass-heavy","Cyberpunk","noise cancel"],
                  "forbidden": ["stretchable","breathable"],
                  "hashtag": "#AudioGear"},
        "gaming": {"keywords": ["gaming","mouse","keyboard","rgb","controller"],
                   "focus": ["No Lag","RGB Setup","Pro-Player","mechanical"],
                   "forbidden": ["cozy","daily wear"],
                   "hashtag": "#GamingSetup"},
        "tech": {"keywords": ["charger","powerbank","cable","adapter","usb"],
                 "focus": ["PD fast charge","Compact","LED indicator"],
                 "forbidden": ["stretch test","real skin"],
                 "hashtag": "#TechLife"},
        "home": {"keywords": ["lamp","organizer","storage","kitchen","furniture"],
                 "focus": ["Aesthetic","space saver","organization"],
                 "forbidden": ["pogi points","RGB"],
                 "hashtag": "#HomeOrganizer"},
        "beauty": {"keywords": ["skincare","makeup","cream","lotion","serum"],
                   "focus": ["Real skin results","texture swatches"],
                   "forbidden": ["heavy-duty","fast-charging"],
                   "hashtag": "#SkincarePH"},
        "motor": {"keywords": ["car","motorcycle","helmet","tire","oil"],
                  "focus": ["Pogi Points","Upgrade","Easy DIY","porma"],
                  "forbidden": ["stretchable","soft fabric"],
                  "hashtag": "#CarAccessories"},
        "sports": {"keywords": ["basketball","mesh","jersey","sports"],
                   "focus": ["Full Sublimation","moisture wicking"],
                   "forbidden": ["fast-charging","RGB"],
                   "hashtag": "#SportsGear"},
        "tools": {"keywords": ["heavy-duty","rechargeable","cordless","handy"],
                  "focus": ["Heavy-duty","High torque","multi-bit"],
                  "forbidden": ["oversized fit","breathable"],
                  "hashtag": "#ToolTime"},
        "pets": {"keywords": ["dog","cat","pet","chew","toy"],
                 "focus": ["Durable","Chew-resistant","non-toxic"],
                 "forbidden": ["fast-charging","RGB"],
                 "hashtag": "#PetLife"}
    }
    
    TAGLISH_PHRASES = [
        ("Grabe ang ganda nito! Sulit na sulit!", "Close-up"),
        ("Solid ang quality mga idol! Presko!", "Texture"),
        ("Sulit na sulit sa presyo! Quality!", "Value"),
        ("Kunin niyo na yung sa'yo! Bilis!", "CTA"),
        ("Kailangan niyo to sa araw-araw!", "Daily use"),
        ("Swerte niyo mga idol! Limited!", "Urgency"),
        ("Panalo to mga boss! Best investment!", "Winner"),
        ("Mura pero quality! Budget-friendly!", "Price")
    ]
    
    CAMERAS = ["Cinematic Pan", "Dynamic Zoom-in", "Handheld POV", "Slow-motion"]
    LIGHTING = ["Soft Studio", "Natural Sunlight", "Neon Glow", "Golden Hour"]
    FRAMING = ["Close-up CU", "Medium Shot MS", "Macro Shot", "Wide Shot WS"]
    def detect_niche(self, title, about, desc):
        text = (title + " " + about + " " + desc).lower()
        for niche, data in self.NICHES.items():
            if any(k in text for k in data["keywords"]):
                return niche
        return "general"
    
    def generate(self, input_data):
        title = input_data.product_title
        about = input_data.about_this_product
        desc = input_data.product_description
        
        niche = self.detect_niche(title, about, desc)
        niche_data = self.NICHES.get(niche, self.NICHES["apparel"])
        duration = random.choice(list(self.DURATIONS.keys()))
        shots = self.DURATIONS[duration]
        
        timings = []
        remaining = duration
        for i in range(shots - 1):
            available = [t for t in self.SHOT_TIMINGS if t <= remaining - 2.1]
            if not available: available = self.SHOT_TIMINGS
            t = random.choice(available)
            timings.append(t)
            remaining -= t
        timings.append(round(remaining, 1))
        
        positives = []
        for i in range(shots):
            taglish, action = self.TAGLISH_PHRASES[i % len(self.TAGLISH_PHRASES)]
            script = f"Shot {i+1:02d} ({timings[i]}s): 4K vertical 9:16 [{self.CAMERAS[i%4]}] [{self.LIGHTING[i%4]}] [{self.FRAMING[i%4]}] Show {niche_data['focus'][i % len(niche_data['focus'])]}. {action}.\nDialogue: \"{taglish}\""
            positives.append(script)
        
        negatives = []
        anti_map = {"Cinematic Pan": "no motion blur", "Dynamic Zoom-in": "no pixelation", "Handheld POV": "stable", "Slow-motion": "fluid"}
        for i in range(shots):
            anti = anti_map.get(self.CAMERAS[i%4], "")
            negatives.append(f"Shot {i+1:02d} Negative: low quality, blurry, distorted, {anti}")

        final_title = f"🔥 MUST-HAVE! {title[:40]} | {niche.upper()} #TikTokMadeMeBuyIt {niche_data['hashtag']}"[:100]
        
        cards = {
            "card1_product_info": {"product_name": title, "category": niche.upper(), "key_features": niche_data["focus"][:3]},
            "card2_video_brief": {"niche": niche, "duration": duration, "shot_count": shots, "target_audience": f"18-35 {niche}"},
            "card3_analysis": {"total_shots": shots, "audio_style": "Taglish VO", "resolution": "4K Vertical"},
            "card4_storyboard": {"shots": [{"shot_num": i+1, "duration": round(timings[i],1), "movement": self.CAMERAS[i%4]} for i in range(shots)]}
        }
        
        gen_id = str(uuid.uuid4())
        if supabase:
            try:
                supabase.table("generation_history").insert({"id": gen_id, "input_field": input_data.dict(), "final_output": {"positive_prompt": "\n\n".join(positives), "negative_prompt": "\n\n".join(negatives), "final_title": final_title}, "created_at": datetime.now().isoformat()}).execute()
            except: pass
            
        return GenerationResponse(id=gen_id, positive_prompt="\n\n".join(positives), negative_prompt="\n\n".join(negatives), final_title=final_title, cards=cards, created_at=datetime.now().isoformat())

ai_core = AITrainingCore()

@app.post("/api/generate", response_model=GenerationResponse)
async def generate_prompt(input_data: ProductInput):
    return ai_core.generate(input_data)

@app.get("/api/history")
async def get_history(limit: int = 100):
    if not supabase: return {"history": []}
    try:
        result = supabase.table("generation_history").select("*").order("created_at", desc=True).limit(limit).execute()
        return {"history": result.data}
    except: return {"history": []}

@app.delete("/api/history/{generation_id}")
async def delete_generation(generation_id: str):
    if not supabase: raise HTTPException(status_code=500, detail="Supabase error")
    supabase.table("generation_history").delete().eq("id", generation_id).execute()
    return {"success": True}

@app.delete("/api/history")
async def delete_all_history():
    if not supabase: raise HTTPException(status_code=500, detail="Supabase error")
    supabase.table("generation_history").delete().neq("id", "").execute()
    return {"success": True}
