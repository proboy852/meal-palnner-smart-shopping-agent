# SmartMeal — AI Meal Planner & Smart Shopping Agent

**Track:** Concierge Agents (Kaggle Agents Intensive)

This repository contains a complete, small-scale implementation of a sequential multi-agent system:
1. **MealPlannerAgent** — creates a weekly meal plan based on user preferences and pantry.
2. **ShoppingListAgent** — converts the meal plan to an itemized shopping list with quantities.
3. **PriceOptimizerAgent** — suggests cheaper alternatives and estimates cost (mock or via SerpAPI).

**Core features included (fulfills Kaggle requirements):**
- Sequential agents (MealPlanner → ShoppingList → PriceOptimizer)
- Memory (stored preferences & pantry in JSON)
- Tools (price lookup: optional real API or mock tool; code execution of helper functions)

---

## Quick demo (run locally)
```bash
python3 -m venv venv
source venv/bin/activate      # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py

## Example: Fallback Run (Offline)
The project includes a fully offline deterministic fallback mode.

Output saved at:
`examples/fallback_run.txt`

This demonstrates:
- Meal planning agent
- Validation agent with auto-correction
- Ingredient extraction agent
- Cost estimation agent
- Final weekly grocery total
