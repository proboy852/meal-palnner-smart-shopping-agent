import os
import random
import ast

USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))
if USE_OPENAI:
    import openai

class MealPlannerAgent:
    def __init__(self, recipes):
        self.recipes = recipes

    def plan_week(self, preferences):
        # Try LLM planner if key present
        if USE_OPENAI:
            try:
                prompt = f"""
You are a meal planner. Use the recipe names list and user preferences to create a 7-day plan.
Recipes: {[r['name'] for r in self.recipes]}
Preferences: {preferences}

Constraints:
- Do not repeat any meal more than twice.
- Honor vegetarian/allergy/disliked items.
Return JSON only like: {{ "Mon":"...", "Tue":"...", ... }}
"""
                resp = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role":"user","content":prompt}],
                    temperature=0.7
                )
                text = resp["choices"][0]["message"]["content"]
                # try to parse JSON-like response
                return ast.literal_eval(text)
            except Exception:
                pass

        # Fallback planner (simple rotation with filters)
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        plan = {}
        vegetarian = preferences.get("vegetarian", False)
        disliked = set(preferences.get("disliked", []))
        allergies = set(preferences.get("allergies", []))

        candidate = []
        for r in self.recipes:
            if r["name"] in disliked:
                continue
            if vegetarian and "vegetarian" not in r.get("tags", []):
                continue
            if allergies & set(r.get("ingredients", {}).keys()):
                continue
            candidate.append(r)

        if not candidate:
            candidate = self.recipes

        for i, d in enumerate(days):
            plan[d] = candidate[i % len(candidate)]["name"]
        return plan
