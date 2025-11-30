import random

class ValidationAgent:
    def validate(self, plan, preferences, recipe_pool):
        problems = []
        suggestion = {}
        seen = {}
        for day, meal in plan.items():
            seen[meal] = seen.get(meal, 0) + 1
        repeats = [m for m,c in seen.items() if c > 2]
        if repeats:
            problems.append(f"Meal repeated too much: {', '.join(repeats)}")
            candidates = [r["name"] for r in recipe_pool if r["name"] not in repeats and (not preferences.get("vegetarian") or "vegetarian" in r.get("tags", []))]
            swaps = {}
            for rep in repeats:
                days = [d for d,m in plan.items() if m==rep]
                for replace_day in days[2:]:
                    alt = candidates.pop(0) if candidates else random.choice([r["name"] for r in recipe_pool if r["name"]!=rep])
                    swaps[replace_day] = alt
            suggestion["swaps"] = swaps
        # vegetarian check
        if preferences.get("vegetarian"):
            nonveg = [d for d,m in plan.items() if "vegetarian" not in next((r for r in recipe_pool if r["name"]==m), {}).get("tags",[])]
            if nonveg:
                problems.append("Plan contains non-vegetarian meals while vegetarian=true")
                vegs = [r["name"] for r in recipe_pool if "vegetarian" in r.get("tags",[])]
                swaps = suggestion.get("swaps",{})
                i=0
                for d in nonveg:
                    swaps[d] = vegs[i % len(vegs)] if vegs else swaps.get(d)
                    i+=1
                suggestion["swaps"]=swaps
        return {"valid": len(problems)==0, "problems": problems, "suggestion": suggestion}
