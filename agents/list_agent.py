import os
import json
USE_GEMINI = bool(os.getenv("GOOGLE_API_KEY"))
if USE_GEMINI:
    import google.generativeai as genai

class ShoppingListAgent:
    def __init__(self, recipes):
        self.recipes = {r["name"]: r for r in recipes}

    def extract_ingredients(self, meal_name):
        if meal_name in self.recipes:
            return self.recipes[meal_name]["ingredients"]
        # If LLM available, ask to infer
        if USE_GEMINI:
            try:
                genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                model = genai.get_model("models/text-bison-001") if hasattr(genai, 'get_model') else genai.GenerativeModel("gemini-pro")
                prompt = f"List ingredients (as JSON) for: {meal_name}. Use grams for quantities."
                if hasattr(genai, 'get_model'):
                    resp = model.generate(prompt=prompt, temperature=0.5)
                    text = resp.text
                else:
                    resp = model.generate_content(prompt)
                    text = resp.text
                start = text.find("{")
                end = text.rfind("}")+1
                return json.loads(text[start:end])
            except Exception:
                pass
        return {"generic_ingredient": 100}

    def generate_list(self, weekly_plan, pantry):
        agg = {}
        for d, meal in weekly_plan.items():
            ing = self.extract_ingredients(meal)
            for item, qty in ing.items():
                need = max(qty - pantry.get(item, 0), 0)
                agg[item] = agg.get(item, 0) + need
        return agg
