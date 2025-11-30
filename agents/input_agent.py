import os

USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))
if USE_OPENAI:
    import openai

class InputUnderstandingAgent:
    """
    Converts messy user text into structured preferences:
    {
      "vegetarian": bool,
      "allergies": [...],
      "disliked": [...],
      "budget": "low/medium/high"
    }
    """

    def parse_input(self, raw_text: str):
        if USE_OPENAI:
            try:
                prompt = f"""
You are an AI that converts messy human text into structured JSON
about food preferences.

User text:
{raw_text}

Return ONLY JSON like this:
{{
 "vegetarian": true/false,
 "allergies": [...],
 "disliked": [...],
 "budget": "low" or "medium" or "high"
}}
"""

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )

                import json
                return json.loads(response["choices"][0]["message"]["content"])

            except Exception:
                pass

        # Fallback without AI
        return {
            "vegetarian": False,
            "allergies": [],
            "disliked": [],
            "budget": "medium"
        }
