import os
from pathlib import Path
import json
import random

USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))
if USE_OPENAI:
    import openai

class MealPlannerAgent:
    def __init__(self, recipes):
        self.recipes = recipes

    def plan_week(self, preferences):
        # If OpenAI exists → AI planning
        if USE_OPENAI:
            try:
                prompt = f"""
Create a creative, healthy weekly meal plan based on:

Preferences:
{preferences}

Recipe list:
{[r['name'] for r in self.recipes]}

Return ONLY JSON like:
{{
 "Mon": "Meal",
 "Tue": "Meal",
 "Wed": "Meal",
 "Thu": "Meal",
 "Fri": "Meal",
 "Sat": "Meal",
 "Sun": "Meal"
}}
"""

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )

                import ast
                return ast.literal_eval(response["choices"][0]["message"]["content"])

            except Exception:
                pass

        # Fallback (no AI)
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        plan = {}
        vegetarian = preferences.get("vegetarian", False)

        filtered = [
            r for r in self.recipes
            if (not vegetarian or "vegetarian" in r["tags"])
        ]

        if not filtered:
            filtered = self.recipes

        for i, d in enumerate(days):
            plan[d] = filtered[i % len(filtered)]["name"]

        return plan
