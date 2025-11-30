import os
import json

USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))
if USE_OPENAI:
    import openai

class InputUnderstandingAgent:
    """
    Converts messy user text into structured preferences.
    """

    def parse_input(self, raw_text: str):
        if USE_OPENAI:
            try:
                prompt = f"""
You are an assistant that converts user cooking preferences into a JSON structure.
User text: {raw_text}
Return ONLY JSON:
{{"vegetarian": true/false, "allergies": [...], "disliked": [...], "budget": "low|medium|high"}}
"""
                resp = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role":"user","content":prompt}],
                    temperature=0.2
                )
                return json.loads(resp["choices"][0]["message"]["content"])
            except Exception:
                pass
        # fallback
        return {"vegetarian": False, "allergies": [], "disliked": [], "budget": "medium"}
