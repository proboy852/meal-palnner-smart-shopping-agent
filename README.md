🌟 AI SmartMeal — LLM-Powered Meal Planner & Smart Grocery Optimization Agent

A multi-agent system for weekly meal planning, ingredient extraction, shopping list generation, and cost optimization with optional Google Gemini LLM support.

🥗 📌 Project Overview

AI SmartMeal is an intelligent, modular, multi-agent system designed to automate the entire weekly meal-planning process:

Meal planning

Ingredient extraction

Pantry comparison

Smart shopping list generation

Price estimation

Plan validation & auto-fixing

Memory of user preferences

The system supports offline fallback mode (no API required) AND LLM-enhanced mode using Google Gemini (gemini-pro) if a GOOGLE_API_KEY is provided.

This makes it:

100% runnable by Kaggle judges

Fully functional offline

Significantly smarter with LLM enabled

🤖 📌 Multi-Agent System Architecture

The project uses a multi-agent architecture, where each specialized agent performs one task and passes information to the next.

1. Input Understanding Agent

Parses user preferences such as:

Vegetarian / non-vegetarian

Budget

Allergies

Disliked ingredients

In LLM mode → can understand natural language preferences (“cheap meals, avoid onions, spicy for dinner”).

2. Meal Planning Agent

Generates a full 7-day weekly meal plan.

In LLM mode → uses Google Gemini to create creative, diverse, non-repetitive plans

Fallback mode → uses deterministic logic from predefined recipes

3. Ingredient Extraction Agent

Converts meals into exact ingredients:

Extracts from predefined recipes

If meal unfamiliar → LLM infers ingredient list

Normalizes quantities

Calculates exact shortages based on pantry

4. Shopping List Aggregation Agent

Combines ingredients from all 7 meals and produces a final list.

The result includes:

Total grams needed

Pantry subtraction

Human-friendly list (g, kg, items)

5. Price Optimization Agent

Uses a tool interface to estimate cost:

Real price lookup if SERPAPI_KEY exists

Mock price fallback for offline mode

Calculates cost per item and total weekly cost

Produces a clear Pandas table

6. Validation & Auto-Fixing Agent

Ensures the plan is valid:

No repeated meals

Vegetarian constraints

Allergy constraints

Logs issues & auto-fixes them

Produces a corrected plan automatically

7. Memory Agent

Stores:

User preferences

Past meal plans

Pantry updates

Makes future runs personalized.

🧠 📌 How the System Works (Flow)
User Input →
Input Understanding Agent →
Meal Planning Agent →
Validation Agent (fixes issues) →
Ingredient Extraction Agent →
Shopping List Agent →
Price Optimization Agent →
Memory Agent → Save / Output


The entire pipeline is orchestrated in main.py.

⚡ 📌 Features at a Glance
✔ Runs fully offline (fallback agents)
✔ Optional LLM mode (Gemini) for real AI reasoning
✔ Auto-fixing of invalid plans
✔ Ingredient inference (LLM-powered)
✔ Price estimation engine
✔ Stores memory between runs
✔ Clean output formatting
✔ Kaggle-ready architecture
✔ Modular multi-agent system
🔧 📌 Installation Instructions
Clone the repo:
git clone https://github.com/YOUR_USERNAME/meal-planner-smart-shopping-agent
cd meal-planner-smart-shopping-agent

Install Python dependencies:
pip install -r requirements.txt


Now you can run:

python main.py

🔐 📌 Optional: Enable Google Gemini LLM Mode

If you want smarter planning, enable Gemini AI:

1. Create a Google API Key

Visit: https://aistudio.google.com

2. Add it to environment variables:

Linux/macOS:

export GOOGLE_API_KEY="your_api_key_here"


Windows PowerShell:

$env:GOOGLE_API_KEY="your_api_key_here"


GitHub Codespaces:

Repository → Settings → Secrets → Codespaces → Add Secret

GOOGLE_API_KEY = your_key_here

Now the system automatically detects and enables LLM mode.

🖥️ 📌 Running the System
Fallback (offline) mode:
python main.py

With Google Gemini:
GOOGLE_API_KEY="your_key_here" python main.py

📊 📌 Example Outputs
🟡 Fallback Output (Offline Mode)

Stored in:

examples/fallback_run.txt


Shows:

Weekly plan

Auto-fixes

Shopping list

Cost table

🔵 LLM Output (Gemini Mode)

Stored in:

examples/llm_run.json


Contains:

LLM prompt

Raw Gemini response

Final parsed JSON plan

📁 📌 Project Structure
agents/           # All agent modules
tools/            # Tool integrations (price lookup)
sample_data/      # Pantry data
examples/         # Fallback & LLM outputs
main.py           # Orchestrator
requirements.txt  # Dependencies
README.md         # Project description
kaggle_writeup.md # Kaggle submission writeup
thumbnail.png     # Kaggle thumbnail

🏆 📌 Why This Project is Kaggle-Ready

This submission satisfies all Kaggle Capstone requirements:

✔ Multi-Agent System

Meal planner, validator, shopping agent, price agent, memory agent.

✔ Tool Usage

Price lookup tool (SerpAPI or mock).

✔ Evaluation Agent

Validation Agent with auto-correction.

✔ Optional LLM Integration

Gemini-powered planning and ingredient inference.

✔ Works Offline

Judges can run it without API keys.

✔ Examples Included

Fallback run

Real LLM run (optional)

📘 📌 How to Reproduce on Kaggle

Open Kaggle Notebook

Import GitHub repo

Run:

!pip install -r requirements.txt
python main.py


(Optional) Add GOOGLE_API_KEY as notebook environment variable

See outputs in terminal

🎯 📌 Future Improvements

Add calorie / nutrition extraction

Add recipe recommendation based on embeddings

Build a Web UI via Streamlit

Auto-fetch real prices from multiple stores

Support hand gesture or voice commands

Meal diversity scoring

❤️ Contributors

Pritam (“ProBoy852”) — Developer

✔ Summary

AI SmartMeal is a full-featured, modular, LLM-powered multi-agent system that automates meal planning and grocery optimization. It is designed to run fully offline for Kaggle judges, while supporting rich Google Gemini-powered reasoning for users with an API key.
