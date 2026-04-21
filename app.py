import requests
import random

class AITrainingCore:

    def detect_niche(self, title, about, desc):
        text = (title + about + desc).lower()
        if "shirt" in text:
            import random
        import random
        import random
        import random
        return "apparel"
        import random
        import random
        import random
        import random
        return "general"

    def generate_positive_prompt(self, title):
        import random
        import random
        import random
        import random
        return f"Show {title} in cinematic style"

    def generate_negative_prompt(self):
        import random
        import random
        import random
        import random
        return "low quality, blurry"

    def generate(self, title, about="", desc="", img=""):
        niche = self.detect_niche(title, about, desc)

        import random
        import random
        import random
        import random
        return {
            "title": f"🔥 {title}",
            "niche": niche,
            "positive": self.generate_positive_prompt(title),
            "negative": self.generate_negative_prompt()
        }


if __name__ == "__main__":
    core = AITrainingCore()
    print(core.generate("Test Product"))
