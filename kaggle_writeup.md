# SmartMeal — AI Meal Planner & Smart Shopping Agent

**Track:** Concierge Agents  
**Author:** Pritam  
**GitHub:** https://github.com/proboy852/meal-planner-smart-shopping-agent  

---

## 1. Problem
Every week, people spend a lot of time deciding:

- “What should I cook today?”
- “Do I already have these ingredients?”
- “Why is my grocery bill so high?”
- “Why do I keep forgetting items and going back to the shop?”

This leads to:
- Time wasted in planning  
- Buying duplicate ingredients  
- Food waste  
- Overspending due to poor planning  
- Repeated meals with low variety  

A well-designed **agent system** can automate this entire workflow.

---

## 2. Solution (What I Built)
**SmartMeal** is a **sequential multi-agent system** that automates weekly meal planning.

It does the following:

1. **MealPlannerAgent**  
   Generates a personalized 7-day weekly meal plan (uses Google Gemini if API key is available, otherwise uses fallback logic).

2. **ShoppingListAgent**  
   Converts the meal plan into a consolidated shopping list considering the user’s pantry.

3. **PriceOptimizerAgent**  
   Estimates total grocery cost using a price lookup tool  
   (mock tool for reproducibility, optional SerpAPI for real prices).

### Key Features
- **Sequential Agent Pipeline:**  
  MealPlanner → ShoppingList → PriceOptimizer  
- **Memory:**  
  Stores user preferences & past plans in `memory.json`  
- **Tools:**  
  Price lookup (mock + optional SerpAPI)  
- **Fallback Mode:**  
  System works **100% offline** without any API keys  
- **Optional LLM Mode:**  
  Automatically uses **Google Gemini** when `GOOGLE_API_KEY` is available

---

## 3. Architecture

### System Flow

### Components
- `main.py` — orchestrates the full pipeline:
  - Load pantry + memory
  - Generate weekly plan
  - Validate & auto-fix plan
  - Produce ingredient list
  - Compute grocery cost

- Memory is persisted in `memory.json` to support:
  - personalization  
  - reproducible behavior  
  - persistent user preferences  

---

## 4. Implementation Highlights

### Technologies Used
- **Python 3**
- **Google Gemini (optional)**  
- **SerpAPI (optional)**  
- **Pandas (cost tables)**
- **Modular agent-based design**

### Code Quality
- Cleanly separated agent classes
- Simple, readable logic
- Each agent handles exactly one responsibility
- Fallback mode ensures reliability

### Documentation
- `README.md` explains how to run the project  
- `examples/` includes both:
  - `fallback_run.txt` (offline example)
  - `llm_run.json` (Gemini example)

---

## 5. Evaluation / Value

### ⏳ Time Saved
Automates the full weekly planning process  
(no more thinking “What should I cook today?”).

### 💸 Cost Savings
PriceOptimizerAgent compares prices and  
suggests cheaper ingredient substitutions.

### 🌱 Sustainability
Uses pantry awareness to:
- reduce duplicate purchases  
- reduce food waste  
- lower total ingredient cost  

### 🤖 AI Enhancement
Using Gemini (optional):
- improves meal diversity  
- generates creative recipes  
- handles dietary constraints better  

---

## 6. How to Run

### **Offline Mode (works for all judges)**
Uses rule-based fallback:
```bash
python main.py
## 7. Bonus & Extensions (Optional)

This project can be extended in multiple directions:

- **Nutrition Analysis:**  
  Add calories, macros, and nutritional scores per meal.

- **Diet Modes:**  
  Support low-carb, high-protein, diabetic-friendly, keto, etc.

- **Real Supermarket Integration:**  
  Connect to APIs like Walmart, BigBasket, Amazon Fresh for:
  - live pricing
  - discounts
  - availability checks

- **UI Improvements:**  
  A Streamlit or Gradio-based dashboard for easy daily use.

- **Voice Interface:**  
  “Plan my meals for the week” → completely hands-free agent.

- **Recipe Expansion:**  
  Link with publicly available recipe datasets or AI-generated recipes.

---

## 8. Reproducibility

To ensure reproducibility for all judges:

- The repository contains a **self-contained demo** with sample:
  - pantry (`sample_data/pantry.json`)
  - recipes
  - fallback output (`examples/fallback_run.txt`)
  - LLM output (`examples/llm_run.json`)

- The entire system works **fully offline** without API keys through a deterministic fallback.

- API-powered features (Gemini, SerpAPI) require keys but are **optional**.

- No API keys are included in the repository. Instructions are provided on how to enable them.

- The system produces the **same output** every time in fallback mode, ensuring:
  - testability  
  - fairness  
  - reproducibility  

---

## Conclusion

SmartMeal is a practical, fully functioning **multi-agent system** that solves a real-world problem: weekly meal planning and grocery optimization.

It successfully demonstrates:

- ✔ **Sequential agents** (MealPlanner → ShoppingList → PriceOptimizer)  
- ✔ **Memory** (persistent user preferences & plan history)  
- ✔ **Tool use** (price lookup tools, optional SerpAPI)  
- ✔ **Fallback reliability** (runs offline with deterministic behavior)  
- ✔ **Optional AI enhancement** (Google Gemini LLM)  

The project is:

- **Realistic** — solves a household problem  
- **Extendable** — easy to add more recipes, budgets, diet types  
- **Reproducible** — judges can run the system with zero setup  
- **Future-proof** — supports LLMs and real-world data sources  

SmartMeal meets all requirements of the **Concierge Agents** track and delivers a clear, well-structured demonstration of agent-based design in action.

