from pathlib import Path
import json
from agents.input_agent import InputUnderstandingAgent
from agents.meal_agent import MealPlannerAgent
from agents.list_agent import ShoppingListAgent, human_friendly_list
from agents.price_agent import PriceOptimizerAgent
from agents.validation_agent import ValidationAgent
from agents.memory_agent import MemoryAgent

# Sample recipes used by the fallback planner
SAMPLE_RECIPES = [
    {"name": "Spaghetti with Tomato Sauce", "ingredients": {"spaghetti":200,"tomato_sauce":150,"olive_oil":10}, "tags":["vegetarian"]},
    {"name": "Chicken Stir Fry", "ingredients": {"chicken":200,"soy_sauce":20,"veg_mix":150,"rice":200}, "tags":[]},
    {"name": "Vegetable Curry", "ingredients": {"potato":200,"carrot":100,"onion":50,"coconut_milk":100}, "tags":["vegetarian"]},
    {"name": "Omelette", "ingredients": {"eggs":2,"milk":30,"salt":1}, "tags":[]},
    {"name": "Salad Bowl", "ingredients": {"lettuce":100,"tomato":50,"cucumber":50,"olive_oil":10}, "tags":["vegetarian"]}
]

PANTRY_FILE = Path("sample_data/pantry.json")

def load_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def run():
    print("=== AI SmartMeal System ===")

    # 0. Prep
    pantry = load_json(PANTRY_FILE)
    mem_agent = MemoryAgent()
    memory = mem_agent.load()
    preferences = memory.get("preferences", {"vegetarian": False, "allergies": [], "disliked": [], "budget": "medium"})

    # 1. Input agent (demo text; in real UI you'd gather user_text)
    ua = InputUnderstandingAgent()
    user_text = "I prefer cheap meals and avoid onions."
    parsed = ua.parse_input(user_text)
    # merge parsed preferences with stored ones
    preferences.update(parsed)

    # 2. Meal planning
    mp = MealPlannerAgent(SAMPLE_RECIPES)
    plan = mp.plan_week(preferences)

    # 3. Validation and auto-fix
    va = ValidationAgent()
    check = va.validate(plan, preferences, SAMPLE_RECIPES)
    if not check["valid"]:
        print("Plan validation failed:", check["problems"])
        swaps = check.get("suggestion", {}).get("swaps", {})
        if swaps:
            print("Applying automatic fixes:", swaps)
            for day, new_meal in swaps.items():
                if day in plan:
                    plan[day] = new_meal
            check2 = va.validate(plan, preferences, SAMPLE_RECIPES)
            if check2["valid"]:
                print("Plan fixed automatically.")
            else:
                print("Still issues after auto-fix:", check2["problems"])
        else:
            print("Using fallback planner.")
            plan = mp.plan_week(preferences)

    # 4. Show plan
    print("\n=== Weekly Plan ===")
    for d,m in plan.items():
        print(f"{d} : {m}")

    # 5. Shopping list
    sla = ShoppingListAgent(SAMPLE_RECIPES)
    shopping = sla.generate_list(plan, pantry)
    print("\n=== Shopping List ===")
    print(human_friendly_list(shopping))

    # 6. Price evaluation
    pa = PriceOptimizerAgent()
    evaluated = pa.evaluate(shopping)
    print("\n=== Cost Table ===")
    print(evaluated["table"].to_string(index=False))
    print(f"\nEstimated total: {evaluated['total_est']}")

    # 7. Save memory
    memory["preferences"] = preferences
    memory["history"].append(plan)
    mem_agent.save(memory)
    print("\nDone. Memory saved.")

if __name__ == "__main__":
    run()
