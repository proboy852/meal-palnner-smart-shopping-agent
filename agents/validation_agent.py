import os
import random

USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))
if USE_OPENAI:
    import openai

class ValidationAgent:
    """
    Validates the plan and tries to auto-fix simple problems:
    - repeated meals
    - vegetarian mismatch
    - allergy conflicts
    """

    def validate(self, plan, preferences, recipe_pool):
        """
        plan: dict day->meal
        preferences: dict of preferences
        recipe_pool: list of recipe dicts (with 'name' and 'tags')
        """
        problems = []
        suggestion = {}
        # check repeats
        seen = {}
        for d, meal in plan.items():
            seen[meal] = seen.get(meal, 0) + 1
        repeats = [m for m,c in seen.items() if c > 2]
        if repeats:
            problems.append(f"Meal repeated too much: {', '.join(repeats)}")
            # build replacement list: choose recipes not repeated and respecting vegetarian/allergy
            candidates = []
            for r in recipe_pool:
                if r["name"] in seen and seen[r["name"]] >= 2:
                    continue
                if preferences.get("vegetarian") and "vegetarian" not in r.get("tags", []):
                    continue
                candidates.append(r["name"])
            # Suggest swaps: replace occurrences past the 2nd with candidates round-robin
            swaps = {}
            for rep in repeats:
                # find days where rep appears after the second occurrence
                days = [d for d,m in plan.items() if m == rep]
                # keep first two, replace the rest
                for replace_day in days[2:]:
                    if not candidates:
                        # fallback: random other recipe
                        alt = random.choice([r["name"] for r in recipe_pool if r["name"] != rep])
                    else:
                        alt = candidates.pop(0)
                    swaps[replace_day] = alt
            suggestion["swaps"] = swaps

        # vegetarian / allergy simple check
        if preferences.get("vegetarian"):
            meat_seen = [m for m in plan.values() if "vegetarian" not in next((r for r in recipe_pool if r["name"]==m), {}).get("tags",[])]
            if meat_seen:
                problems.append("Plan contains non-vegetarian meals while vegetarian=true")
                # suggestion: swap those days with vegetarian recipes
                vegs = [r["name"] for r in recipe_pool if "vegetarian" in r.get("tags",[])]
                swaps = suggestion.get("swaps",{})
                i = 0
                for d,m in list(plan.items()):
                    if m in meat_seen:
                        swaps[d] = vegs[i % len(vegs)] if vegs else swaps.get(d, m)
                        i += 1
                suggestion["swaps"] = swaps

        valid = len(problems) == 0
        return {"valid": valid, "problems": problems, "suggestion": suggestion}
