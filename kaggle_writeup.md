# SmartMeal — AI Meal Planner & Smart Shopping Agent

**Track:** Concierge Agents  
**Author:** (Your Name)  
**GitHub Repo:** https://github.com/YOUR-USERNAME/meal-planner-smart-shopping-agent

---

## 1. Problem Statement

Meal planning and grocery organization are repetitive tasks that consume time and energy.  
People face several issues:

- Difficulty deciding meals for the week  
- Forgetting items while shopping  
- Buying duplicates due to poor pantry tracking  
- Overspending because no price comparison is done  

A simple multi-agent system can remove this burden and make weekly planning efficient.

---

## 2. Solution Overview

SmartMeal is a **three-agent sequential system**:

### 🥗 **1. MealPlannerAgent**
Creates a 7-day weekly meal plan based on:
- User preferences  
- Recipes  
- Pantry items  
- Allergies/dislikes  
- Memory of past meal plans  

### 🛒 **2. ShoppingListAgent**
Converts the weekly meal plan into:
- A complete shopping list  
- Correct ingredient quantities  
- Deducts items already available in pantry  

### 💰 **3. PriceOptimizerAgent**
Uses a **tool** to:
- Estimate price for each item  
- Provide alternative cost-friendly options  
- Calculate total estimated shopping cost  

This helps users:
- Save time  
- Reduce food waste  
- Save money  

---

## 3. Key Kaggle Requirements Implemented

SmartMeal includes **more than 3** required AI agent concepts:

### ✔ **Sequential Agents**  
(Agent 1 → Agent 2 → Agent 3)

### ✔ **Tools**  
Price lookup tool (mock price lookup or SerpAPI if enabled)

### ✔ **Memory**  
- Pantry saved in `pantry.json`  
- User preferences stored in `memory.json`  
- Past meal history saved  

### ✔ **Context Engineering**  
Agents use pantry + preferences to filter valid meals.

### ✔ **Agent Evaluation**  
The system prints:
- Meal plan  
- Shopping list  
- Estimated cost  

---

## 4. Architecture Diagram (Text Version)

User Preferences + Pantry
↓
MealPlannerAgent
↓
Weekly Meal Plan (7 days)
↓
ShoppingListAgent
↓
List of Items Needed + Qty
↓
PriceOptimizerAgent (Tool)
↓
Cost Estimate + Store Suggestions

---

## 5. Implementation Details

The entire system is implemented in `main.py`.

### Files:
- `main.py` → Full agent pipeline  
- `sample_data/pantry.json` → Pantry data  
- `memory.json` → Created automatically  
- `requirements.txt` → Dependencies  
- `README.md` → Instructions  

### Technology used:
- Python 3  
- Optional OpenAI (if API key added)  
- Optional SerpAPI (if key added)  

The default demo runs fully **offline** using mock data.

---

## 6. Running the Project

Install requirements (only needed if you want to run the code locally):

pip install -r requirements.txt

Run:

python main.py

yaml
Copy code

It will print:

1. Weekly meal plan  
2. Aggregated shopping list  
3. Estimated shopping cost  

---

## 7. Value & Impact

SmartMeal helps users:

- Reduce time spent planning meals  
- Stay organized  
- Avoid unnecessary purchases  
- Save money with cost optimization  
- Reduce food waste  
- Maintain consistent meal habits with history-based memory  

Simple, effective, and very practical.

---

## 8. Bonus Features (Optional)

- Add nutrition tracking  
- Add real recipes using an API  
- Add real supermarket prices  
- Deploy as a web app  
- Add voice control  

---

## 9. Conclusion

SmartMeal is a practical, easy-to-run multi-agent system built using:
- Sequential agents  
- Tool usage  
- Memory  
- Context engineering  

It meets Kaggle’s Capstone submission requirements and provides real-world value in meal planning and grocery shopping.

---
