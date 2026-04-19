class TikTokPrompt:
    @staticmethod
    def build(title, description, product_details, custom_instruction):
        """Builds structured prompt for TikTok product analysis"""
        
        base_prompt = f"""
You are a TikTok content strategist. Analyze this product and create viral content.

PRODUCT INFORMATION:
Title: {title}
Description: {description}
Details: {product_details}

TASK: Create a TikTok prompt that will make this product go viral.

OUTPUT FORMAT (must follow exactly):
--- 
Hook: [Attention-grabbing first 3 seconds]
Problem Solved: [What pain point this addresses]
Emotional Angle: [Why viewers will care]
Call to Action: [What viewers should do]
Hashtags: [5 relevant hashtags]
---

{custom_instruction if custom_instruction else "Focus on emotional appeal and relatability."}
"""
        return base_prompt

class StructuredOutputPrompt:
    @staticmethod
    def for_json(title, description, image_url):
        """Returns structured JSON output"""
        return f"""
Analyze this TikTok product and return ONLY valid JSON with no other text:
{{
    "product_name": "{title}",
    "virality_score": [1-10],
    "target_audience": "...",
    "best_audio_suggestion": "...",
    "caption_template": "..."
}}
"""
