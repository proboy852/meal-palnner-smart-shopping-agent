import os
import json

USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))
if USE_OPENAI:
    import openai

class ShoppingListAgent:
    """
    LLM extracts ingredients from ANY meal name.
    """

    def __init__(self, recipes):
        self.recipes = {r["name"]: r for r in recipes}

    def extract_ingredients(self, meal_name):
        # If meal is known in recipe list:
        if meal_name in self.recipes:
            return self.recipes[meal_name]["ingredients"]

        # Else use AI to infer ingredients
        if USE_OPENAI:
            prompt = f"""
Given the meal name "{meal_name}", infer realistic ingredients.

Return ONLY JSON like:
{{
 "ingredient": quantity (integer grams)
}}
"""

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                import json
                return json.loads(response["choices"][0]["message"]["content"])
            except:
                pass

        # Fallback default
        return {"generic_ingredient": 100}

    def generate_list(self, weekly_plan, pantry):
        shopping = {}
        for day, meal in weekly_plan.items():
            ing = self.extract_ingredients(meal)
            for item, qty in ing.items():
                need = max(qty - pantry.get(item, 0), 0)
                shopping[item] = shopping.get(item, 0) + need
        return shopping
