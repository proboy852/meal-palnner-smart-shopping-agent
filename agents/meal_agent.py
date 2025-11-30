import os
import json

USE_GEMINI = bool(os.getenv("GOOGLE_API_KEY"))

if USE_GEMINI:
    import google.generativeai as genai

class MealPlannerAgent:
    def __init__(self, recipes):
        self.recipes = recipes

    def plan_week(self, preferences):
        if USE_GEMINI:
            try:
                genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                model = genai.get_model("models/text-bison-001") if hasattr(genai, 'get_model') else genai.GenerativeModel("gemini-pro")
                prompt = f"""
You are a meal planning assistant. Create a 7-day weekly meal plan (Mon-Sun) in JSON.
Constraints:
- Do not repeat any meal more than once.
- Respect vegetarian={preferences.get('vegetarian')}.
- Use only meals from this list or common simple meals.
Return only valid JSON object with day keys.
Available recipes: {[r['name'] for r in self.recipes]}
"""
                # compatibility for older/newer google SDK usage:
                if hasattr(genai, 'get_model'):
                    resp = model.generate(prompt=prompt, temperature=0.7)
                    text = resp.text
                else:
                    resp = model.generate_content(prompt)
                    text = resp.text
                # extract JSON
                start = text.find("{")
                end = text.rfind("}") + 1
                j = json.loads(text[start:end])
                return j
            except Exception as e:
                print("[Gemini error — falling back]", e)

        # fallback deterministic planner
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        candidate = [r for r in self.recipes if (not preferences.get("vegetarian") or "vegetarian" in r.get("tags", []))]
        if not candidate:
            candidate = self.recipes
        plan = {}
        for i,d in enumerate(days):
            plan[d] = candidate[i % len(candidate)]["name"]
        return plan
