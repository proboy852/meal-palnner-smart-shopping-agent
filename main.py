from pathlib import Path
import json
from agents.input_agent import InputUnderstandingAgent
from agents.meal_agent import MealPlannerAgent
from agents.list_agent import ShoppingListAgent
from agents.price_agent import PriceOptimizerAgent
from agents.validation_agent import ValidationAgent
from agents.memory_agent import MemoryAgent
import pandas as pd
import os

BASE = Path(__file__).parent
PANTRY_FILE = BASE / "sample_data" / "pantry.json"

SAMPLE_RECIPES = [
    {"name":"Spaghetti with Tomato Sauce","ingredients":{"spaghetti":200,"tomato_sauce":150,"olive_oil":10},"tags":["vegetarian"]},
    {"name":"Chicken Stir Fry","ingredients":{"chicken":200,"soy_sauce":20,"veg_mix":150,"rice":200},"tags":[]},
    {"name":"Vegetable Curry","ingredients":{"potato":200,"carrot":100,"onion":50},"tags":["vegetarian"]},
    {"name":"Omelette","ingredients":{"eggs":2,"milk":30,"salt":1},"tags":[]},
    {"name":"Salad Bowl","ingredients":{"lettuce":100,"tomato":50,"cucumber":50,"olive_oil":10},"tags":["vegetarian"]}
]

def load_json(p):
    if not p.exists(): return {}
    return json.loads(p.read_text())

def human_friendly_list(shopping):
    lines=[]
    for item,qty in shopping.items():
        if qty<=0: continue
        if qty>=1000: qty_str=f"{qty/1000:.1f} kg"
        elif qty>=100: qty_str=f"{qty} g"
        else: qty_str=f"{qty} g"
        lines.append(f"- {item}: {qty_str}")
    return "\n".join(lines)

def run():
    print("=== AI SmartMeal System ===")
    pantry = load_json(PANTRY_FILE)
    mema = MemoryAgent()
    memory = mema.load()
    preferences = memory.get("preferences", {"vegetarian":False,"allergies":[],"disliked":[],"budget":"medium"})

    # Input (demo)
    ua = InputUnderstandingAgent()
    user_text = "I want cheap food, avoid onion, and make 2 vegetarian meals."
    parsed = ua.parse_input(user_text)
    preferences.update(parsed)

    # Meal planning
    mp = MealPlannerAgent(SAMPLE_RECIPES)
    plan = mp.plan_week(preferences)

    # Validation and auto-fix
    va = ValidationAgent()
    check = va.validate(plan, preferences, SAMPLE_RECIPES)
    if not check["valid"]:
        print("Plan validation failed:", check["problems"])
        swaps = check.get("suggestion",{}).get("swaps",{})
        if swaps:
            print("Applying automatic fixes:", swaps)
            for day,new in swaps.items():
                if day in plan:
                    plan[day]=new
            check2 = va.validate(plan, preferences, SAMPLE_RECIPES)
            if check2["valid"]:
                print("Plan fixed automatically.")
            else:
                print("Still issues after auto-fix:", check2["problems"])
        else:
            print("No automatic fixes — falling back to deterministic planner.")
            plan = mp.plan_week(preferences)

    print("\n=== Weekly Plan ===")
    for d,m in plan.items():
        print(d, ":", m)

    # Shopping list
    sla = ShoppingListAgent(SAMPLE_RECIPES)
    shopping = sla.generate_list(plan, pantry)
    print("\n=== Shopping List ===")
    print(human_friendly_list(shopping))

    # Price optimization
    pa = PriceOptimizerAgent()
    evaluated = pa.evaluate(shopping)
    print("\n=== Cost Table ===")
    print(evaluated["table"].to_string(index=False))
    print("\nEstimated total:", evaluated["total_est"])

    # Save memory + outputs
    memory["preferences"]=preferences
    memory["history"].append({"date":str(pd.Timestamp.now()), "plan": plan})
    mema.save(memory)
    # Save last run results as fallback_run.txt for reproducibility
    BASE.joinpath("examples").mkdir(exist_ok=True)
    BASE.joinpath("examples","fallback_run.txt").write_text(
        "=== AI SmartMeal System ===\nPlan (saved output):\n" + json.dumps(plan, indent=2) + "\n\nEstimated total: " + str(evaluated["total_est"])
    )
    print("\nDone. Memory saved. Fallback run written to examples/fallback_run.txt")

if __name__ == "__main__":
    run()
