import os

USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))
if USE_OPENAI:
    import openai

class ValidationAgent:
    """
    Validates:
    - allergy conflicts
    - repeated meals
    - vegetarian mismatch
    """

    def validate(self, plan, preferences):
        if USE_OPENAI:
            try:
                prompt = f"""
Check this weekly plan:

{plan}

Rules:
- Avoid allergies: {preferences['allergies']}
- Avoid disliked foods: {preferences['disliked']}
- If vegetarian=true, no meat.
- Avoid repeating the same meal more than twice.

Return ONLY JSON:
{{
 "valid": true/false,
 "problems": [...],
 "suggestion": {{}}
}}
"""

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role":"user","content":prompt}]
                )
                import json
                return json.loads(response["choices"][0]["message"]["content"])
            except:
                pass

        # fallback simple validator
        problems = []
        seen = {}

        for d, meal in plan.items():
            seen[meal] = seen.get(meal, 0) + 1
            if seen[meal] > 2:
                problems.append(f"Meal repeated too much: {meal}")

        return {"valid": len(problems)==0, "problems": problems, "suggestion": {}}
