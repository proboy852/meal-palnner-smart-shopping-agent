from agents.input_agent import InputUnderstandingAgent
from agents.meal_agent import MealPlannerAgent
from agents.list_agent import ShoppingListAgent
from agents.price_agent import PriceOptimizerAgent
from agents.validation_agent import ValidationAgent
from agents.memory_agent import MemoryAgent

from pathlib import Path
import json

RECIPES_FILE = Path("sample_data/recipes.json")
PANTRY_FILE = Path("sample_data/pantry.json")

SAMPLE_RECIPES = [
    {"name": "Spaghetti with Tomato Sauce", "ingredients": {"spaghetti":200, "tomato_sauce":150}, "tags":["vegetarian"]},
    {"name": "Chicken Stir Fry", "ingredients": {"chicken":200,"soy_sauce":20,"veg_mix":150,"rice":200}, "tags":[]},
    {"name": "Vegetable Curry", "ingredients": {"potato":200,"carrot":100,"onion":50}, "tags":["vegetarian"]},
]

def load_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def run():
    print("=== AI SmartMeal System ===")

    # Load pantry
    pantry = load_json(PANTRY_FILE)

    # Load memory
    mema = MemoryAgent()
    memory = mema.load()
    preferences = memory.get("preferences", {
        "vegetarian": False,
        "allergies": [],
        "disliked": [],
        "budget": "medium"
    })

    # 1. INPUT AGENT
    ua = InputUnderstandingAgent()
    user_text = "I want cheap food, avoid onion, and make 2 vegetarian meals."
    parsed_preferences = ua.parse_input(user_text)
    preferences.update(parsed_preferences)

    # 2. MEAL PLANNING
    mp = MealPlannerAgent(SAMPLE_RECIPES)
    plan = mp.plan_week(preferences)

    # 3. VALIDATION
    va = ValidationAgent()
    check = va.validate(plan, preferences)

    if not check["valid"]:
        print("Plan validation failed:", check["problems"])
        print("Using fallback rules.")
        plan = mp.plan_week(preferences)

    print("\n=== Weekly Plan ===")
    for d,m in plan.items():
        print(d,":",m)

    # 4. SHOPPING LIST
    sla = ShoppingListAgent(SAMPLE_RECIPES)
    shopping = sla.generate_list(plan, pantry)

    print("\n=== Shopping List ===")
    for i,q in shopping.items():
        print(i,":",q)

    # 5. PRICE OPTIMIZATION
    pa = PriceOptimizerAgent()
    result = pa.evaluate(shopping)

    print("\n=== Cost Table ===")
    print(result["table"].to_string(index=False))

    print("\nEstimated total:", result["total_est"])

    # 6. MEMORY SAVE
    memory["preferences"] = preferences
    memory["history"].append(plan)
    mema.save(memory)

if __name__ == "__main__":
    run()
