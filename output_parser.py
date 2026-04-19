import re

class TikTokOutputParser:
    @staticmethod
    def parse(model_response):
        hook_match = re.search(r"Hook:\s*(.+?)(?=\n|$)", model_response)
        problem_match = re.search(r"Problem Solved:\s*(.+?)(?=\n|$)", model_response)
        emotional_match = re.search(r"Emotional Angle:\s*(.+?)(?=\n|$)", model_response)
        cta_match = re.search(r"Call to Action:\s*(.+?)(?=\n|$)", model_response)
        hashtags_match = re.search(r"Hashtags:\s*(.+?)(?=\n|$)", model_response)
        
        formatted = f"""
═══════════════════════════════════════
📱 TIKTOK PROMPT GENERATED
═══════════════════════════════════════

🔥 HOOK:
{hook_match.group(1) if hook_match else "N/A"}

💡 PROBLEM SOLVED:
{problem_match.group(1) if problem_match else "N/A"}

❤️ EMOTIONAL ANGLE:
{emotional_match.group(1) if emotional_match else "N/A"}

🎯 CALL TO ACTION:
{cta_match.group(1) if cta_match else "N/A"}

#️⃣ HASHTAGS:
{hashtags_match.group(1) if hashtags_match else "N/A"}

═══════════════════════════════════════
"""
        return formatted
