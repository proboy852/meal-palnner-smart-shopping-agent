
# main.py (full code)
Create `main.py` with the following code. It is self-contained and runnable offline; it also includes clear hooks to enable real LLM and real web price tool.

> Note: **DO NOT** include API keys in the repo. Use environment variables like `OPENAI_API_KEY` and `SERPAPI_KEY` when enabling live services.

```python
"""
SmartMeal — Meal Planner + Shopping List + Price Optimizer
Demonstrates:
- Sequential agents
- Memory (simple JSON file)
- Tools (price lookup tool - mock or via SerpAPI)
"""

import json
import os
import random
from pathlib import Path
from typing import List, Dict
import datetime
import pandas as pd

# Optional LLM (OpenAI) integration if you set OPENAI_API_KEY
USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))

if USE_OPENAI:
    import openai

# Optional SerpAPI (for price lookup) if you set SERPAPI_KEY
USE_SERPAPI = bool(os.getenv("SERPAPI_KEY"))
if USE_SERPAPI:
    import requests

BASE_DIR = Path(__file__).parent
PANTRY_FILE = BASE_DIR / "sample_data" / "pantry.json"
MEMORY_FILE = BASE_DIR / "memory.json"

# -------------------------
# Utilities / Memory (simple)
# -------------------------
def load_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))

def load_memory():
    mem = load_json(MEMORY_FILE)
    if not mem:
        mem = {"preferences": {"vegetarian": False, "allergies": [], "disliked": []}, "history": []}
        save_json(MEMORY_FILE, mem)
    return mem

def update_memory(key, value):
    mem = load_memory()
    mem[key] = value
    save_json(MEMORY_FILE, mem)

# -------------------------
# Sample recipe dataset (minimal)
# -------------------------
SAMPLE_RECIPES = [
    {"name": "Spaghetti with Tomato Sauce", "ingredients": {"spaghetti":200,"tomato_sauce":150,"olive_oil":10}, "tags":["vegetarian"]},
    {"name": "Chicken Stir Fry", "ingredients": {"chicken":200,"soy_sauce":20,"veg_mix":150,"rice":200}, "tags":[]},
    {"name": "Vegetable Curry", "ingredients": {"potato":200,"carrot":100,"onion":50,"coconut_milk":100}, "tags":["vegetarian"]},
    {"name": "Omelette", "ingredients": {"eggs":2,"milk":30,"salt":1}, "tags":[]},
    {"name": "Salad Bowl", "ingredients": {"lettuce":100,"tomato":50,"cucumber":50,"olive_oil":10}, "tags":["vegetarian"]},
]

# -------------------------
# Tools
# -------------------------
def mock_price_lookup(item_name: str) -> Dict:
    """Mock price lookup tool: returns a fake price and store."""
    price = round(random.uniform(0.5, 5.0) * len(item_name.split()), 2)
    return {"item": item_name, "price": price, "store": "MockMart"}

def serpapi_price_lookup(item_name: str) -> Dict:
    """(Optional) Real price lookup via SerpAPI - requires SERPAPI_KEY
    NOTE: This function is optional and not enabled by default.
    """
    key = os.getenv("SERPAPI_KEY")
    if not key:
        return mock_price_lookup(item_name)
    # Example using Google Shopping (SerpAPI).
    params = {"q": item_name, "api_key": key, "engine": "google_shopping"}
    resp = requests.get("https://serpapi.com/search", params=params, timeout=10)
    data = resp.json()
    # parse a price if available
    try:
        value = data.get("shopping_results", [])[0]
        price_str = value.get("price", "")
        # crude price parse
        price = float(''.join(ch for ch in price_str if (ch.isdigit() or ch=='.')))
        store = value.get("source", "Store")
    except Exception:
        return mock_price_lookup(item_name)
    return {"item": item_name, "price": price, "store": store}

def price_lookup(item_name: str):
    if USE_SERPAPI:
        return serpapi_price_lookup(item_name)
    else:
        return mock_price_lookup(item_name)

# -------------------------
# Agents
# -------------------------
class MealPlannerAgent:
    """Create a weekly meal plan using preferences, pantry, and recipes."""
    def __init__(self, recipes):
        self.recipes = recipes

    def plan_week(self, preferences: Dict, pantry: Dict) -> Dict[str, List]:
        # If OpenAI enabled, we could call LLM for richer planning.
        # For now create a simple planner:
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        plan = {}
        vegetarian = preferences.get("vegetarian", False)
        disliked = set(preferences.get("disliked", []))
        allergies = set(preferences.get("allergies", []))

        candidate_recipes = []
        for r in self.recipes:
            tags = set(r.get("tags", []))
            # skip allergy/disliked matches (simple)
            if allergies & set(r["ingredients"].keys()):
                continue
            if r["name"] in disliked:
                continue
            if vegetarian and "vegetarian" not in tags:
                continue
            candidate_recipes.append(r)

        if not candidate_recipes:
            candidate_recipes = self.recipes  # fallback

        # Simple rotation
        for i, d in enumerate(days):
            plan[d] = candidate_recipes[i % len(candidate_recipes)]["name"]
        return plan

class ShoppingListAgent:
    """Convert a meal plan into an aggregated shopping list based on recipes."""
    def __init__(self, recipes):
        self.recipes = {r["name"]: r for r in recipes}

    def generate_list(self, plan: Dict[str,str], pantry: Dict[str,int]) -> Dict[str, float]:
        agg = {}
        for day, meal in plan.items():
            recipe = self.recipes.get(meal)
            if not recipe:
                continue
            for ing, qty in recipe["ingredients"].items():
                have = pantry.get(ing, 0)
                need = max(qty - have, 0)
                agg[ing] = agg.get(ing, 0) + need
        return agg

class PriceOptimizerAgent:
    """Look up prices and suggest cheaper alternatives."""
    def __init__(self, price_tool):
        self.price_tool = price_tool

    def evaluate(self, shopping_list: Dict[str, float]):
        rows = []
        total_est = 0.0
        for item, qty in shopping_list.items():
            p = self.price_tool(item)
            est = p["price"] * (qty / 100.0 if qty>10 else 1)  # heuristic
            rows.append({ "item": item, "qty": qty, "unit_price": p["price"], "store": p["store"], "est_cost": round(est,2)})
            total_est += est
        return {"items": rows, "total_est": round(total_est,2)}

# -------------------------
# Runner / Orchestration (sequential)
# -------------------------
def run_demo():
    print("SmartMeal — Demo starting")

    # Load memory or initialize
    mem = load_memory()
    # load sample pantry
    pantry_data = load_json(PANTRY_FILE) or {"tomato_sauce": 100, "spaghetti": 0, "eggs": 1}
    print("Loaded pantry:", pantry_data)
    print("Loaded memory/preferences:", mem["preferences"])

    # Agent 1: Meal planning
    mp = MealPlannerAgent(SAMPLE_RECIPES)
    plan = mp.plan_week(mem["preferences"], pantry_data)
    print("\n=== Weekly Meal Plan ===")
    for day, meal in plan.items():
        print(day, ":", meal)

    # Save plan to memory history
    mem["history"].append({"date": str(datetime.date.today()), "plan": plan})
    save_json(MEMORY_FILE, mem)

    # Agent 2: Shopping list
    sl = ShoppingListAgent(SAMPLE_RECIPES)
    shopping_list = sl.generate_list(plan, pantry_data)
    print("\n=== Shopping List (aggregated quantities) ===")
    for item, qty in shopping_list.items():
        print(f"{item}: {qty}")

    # Agent 3: Price optimization (tool)
    po = PriceOptimizerAgent(price_lookup)
    evaluated = po.evaluate(shopping_list)
    print("\n=== Price Evaluation (estimates) ===")
    df = pd.DataFrame(evaluated["items"])
    print(df.to_string(index=False))
    print("\nEstimated total cost:", evaluated["total_est"])

    print("\nDemo complete. Memory saved to", MEMORY_FILE)

if __name__ == "__main__":
    run_demo()
