import random
import os

USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))
if USE_OPENAI:
    import openai

class ValidationAgent:
    def validate(self, plan, preferences, recipe_pool):
        problems = []
        suggestion = {}
        seen = {}
        for d, meal in plan.items():
            seen[meal] = seen.get(meal, 0) + 1
        repeats = [m for m, c in seen.items() if c > 2]
        if repeats:
            problems.append(f"Meal repeated too much: {', '.join(repeats)}")
            # build replacements
            candidates = []
            for r in recipe_pool:
                if r["name"] in seen and seen[r["name"]] >= 2:
                    continue
                if preferences.get("vegetarian") and "vegetarian" not in r.get("tags", []):
                    continue
                candidates.append(r["name"])
            swaps = {}
            for rep in repeats:
                days = [d for d, m in plan.items() if m == rep]
                for replace_day in days[2:]:
                    if candidates:
                        alt = candidates.pop(0)
                    else:
                        alt = random.choice([r["name"] for r in recipe_pool if r["name"] != rep])
                    swaps[replace_day] = alt
            suggestion["swaps"] = swaps

        # vegetarian check
        if preferences.get("vegetarian"):
            nonveg = [m for m in plan.values() if not any("vegetarian" in r.get("tags", []) and r["name"]==m for r in recipe_pool)]
            if nonveg:
                problems.append("Plan contains non-vegetarian meals while vegetarian=true")
                vegs = [r["name"] for r in recipe_pool if "vegetarian" in r.get("tags",[])]
                swaps = suggestion.get("swaps", {})
                i = 0
                for d, m in list(plan.items()):
                    if m in nonveg:
                        swaps[d] = vegs[i % len(vegs)] if vegs else swaps.get(d, m)
                        i += 1
                suggestion["swaps"] = swaps

        valid = len(problems) == 0
        return {"valid": valid, "problems": problems, "suggestion": suggestion}
