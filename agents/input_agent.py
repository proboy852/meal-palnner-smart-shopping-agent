import os
USE_OPENAI = False  # not used if we use Gemini; kept for compatibility

class InputUnderstandingAgent:
    def parse_input(self, raw_text: str):
        # Simple parser fallback: returns default structured preferences
        raw = (raw_text or "").lower()
        return {
            "vegetarian": "vegetarian" in raw or "veg" in raw,
            "allergies": [],
            "disliked": [],
            "budget": "low" if "cheap" in raw or "low budget" in raw else "medium"
        }
