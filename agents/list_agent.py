import os
import json

USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))
if USE_OPENAI:
    import openai

class ShoppingListAgent:
    def __init__(self, recipes):
        self.recipes = {r["name"]: r for r in recipes}

    def extract_ingredients(self, meal_name):
        # Known recipe
        if meal_name in self.recipes:
            return self.recipes[meal_name].get("ingredients", {})
        # Use LLM to infer ingredients
        if USE_OPENAI:
            try:
                prompt = f"""
Given the meal name: "{meal_name}", infer a reasonable JSON of ingredient:grams or count.
Return JSON only.
"""
                resp = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role":"user","content":prompt}],
                    temperature=0.6
                )
                return json.loads(resp["choices"][0]["message"]["content"])
            except Exception:
                pass
        # Fallback
        return {"generic_ingredient": 150}

    def generate_list(self, weekly_plan, pantry):
        agg = {}
        for day, meal in weekly_plan.items():
            ing = self.extract_ingredients(meal)
            for item, qty in ing.items():
                need = max(qty - pantry.get(item, 0), 0)
                agg[item] = agg.get(item, 0) + need
        return agg

def human_friendly_list(shopping_dict):
    lines = []
    for item, qty in shopping_dict.items():
        if qty <= 0:
            continue
        if qty >= 1000:
            qty_str = f"{qty/1000:.1f} kg"
        elif qty >= 100:
            qty_str = f"{qty} g"
        else:
            qty_str = f"{qty} g"
        lines.append(f"- {item}: {qty_str}")
    return "\n".join(lines)
