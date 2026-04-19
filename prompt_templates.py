class TikTokPrompt:
    @staticmethod
    def build(title, description, product_details, custom_instruction):
        base_prompt = f"""
You are a TikTok content strategist. Analyze this product and create viral content.

PRODUCT INFORMATION:
Title: {title}
Description: {description}
Details: {product_details}

OUTPUT FORMAT:
Hook: [Attention-grabbing first 3 seconds]
Problem Solved: [What pain point this addresses]
Emotional Angle: [Why viewers will care]
Call to Action: [What viewers should do]
Hashtags: [5 relevant hashtags]

{custom_instruction if custom_instruction else "Focus on emotional appeal."}
"""
        return base_prompt
