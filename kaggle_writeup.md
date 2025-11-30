# 🧠 AI SmartMeal — Multi-Agent Weekly Meal Planner & Smart Grocery Optimizer  
### Track: Concierge Agents

---

## 🎯 Problem Overview  
Weekly meal planning is time-consuming and mentally exhausting.  
Users struggle with:

- deciding what to cook every day  
- managing dietary needs (vegetarian, allergies, dislikes)  
- keeping track of pantry items  
- minimizing grocery cost  
- avoiding repeated meals  
- planning a balanced weekly rotation  

This project demonstrates a **multi-agent system** that solves this end-to-end.

---

## 🤖 Multi-Agent Architecture  

### **1. Input Understanding Agent**  
Extracts user preferences from messy text.  
Example input:  
> “I want cheap food, avoid onion, and include some vegetarian meals.”

Result:
```json
{
  "vegetarian": false,
  "allergies": [],
  "disliked": [],
  "budget": "low"
}
2. Meal Planning Agent
Plans a 7-day meal schedule.

Uses Google Gemini if an API key is available

Otherwise uses a deterministic fallback

Ensures no meal repeats more than once

Respects preferences like vegetarian or disliked items

A real Gemini example is stored in:

bash
Copy code
examples/llm_run.json
and a fallback example is stored in:

bash
Copy code
examples/fallback_run.txt
3. Ingredient Extraction Agent
For each meal, builds an ingredient list:

If meal is known: use database

If unknown: Gemini infers ingredients (optional)

Always works offline through fallback mode

4. Shopping List Agent
Aggregates ingredient quantities for the entire week.

Example output:

diff
Copy code
- spaghetti: 600 g
- tomato_sauce: 150 g
- chicken: 400 g
...
5. Price Optimization Agent
A tool-use agent that:

Fetches real prices from SerpAPI (optional)

Otherwise uses mock price data

Outputs estimated total grocery cost

Example output is shown as a table (pandas DataFrame).

6. Validation Agent
Checks for:

repeated meals

non-vegetarian meals (if vegetarian mode)

allergy-triggering recipes

Automatically fixes invalid plans by swapping meals intelligently.

7. Memory Agent
Stores:

user preferences

previously generated meal plans

This enables personalization across sessions.

🏗️ System Flow
Parse user text → structured preferences

Generate weekly meal plan

Validate + auto-correct

Extract ingredients

Build shopping list

Estimate grocery cost

Save memory

📄 Example Outputs
Fallback Mode (Always Works Offline)
A full fallback example is included in:

bash
Copy code
examples/fallback_run.txt
This ensures judges can run the project without API keys.

Gemini LLM Mode (Optional)
If GOOGLE_API_KEY is added, the system produces:

more diverse meal plans

improved ingredients

smarter substitutions

The real LLM output is saved in:

bash
Copy code
examples/llm_run.json
🔧 Implementation
The system is structured as:

css
Copy code
agents/
    input_agent.py
    meal_agent.py
    list_agent.py
    price_agent.py
    validation_agent.py
    memory_agent.py
tools/
    price_lookup.py
examples/
    fallback_run.txt
    llm_run.json
main.py
requirements.txt
README.md
kaggle_writeup.md
Runs offline, with optional LLM enhancements.

🛠️ Running the Project
Offline / Fallback Mode (recommended for judges)
css
Copy code
python main.py
Gemini LLM Mode
Add environment variable:

makefile
Copy code
GOOGLE_API_KEY=your_key_here
python main.py
💡 Why This Project Matters
This project demonstrates:

AI planning

tool-use

multi-agent reasoning

memory

validation and auto-correction

cost optimization

optional LLM integration

It solves a real-world problem in a structured, reproducible way.

🏁 Conclusion
AI SmartMeal highlights how multi-agent systems can simplify complex daily routines.

It successfully:

generates meal plans

validates and corrects them

extracts ingredients

optimizes cost

supports both offline and AI-enhanced modes

This fulfills the goals of the Concierge Agent Track and presents a complete, reproducible multi-agent pipeline.
