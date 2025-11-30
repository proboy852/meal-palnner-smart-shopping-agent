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
# Meal Planning Agent (Gemini + fallback)
plan = {
  "Mon": "Spaghetti with Tomato Sauce",
  "Tue": "Chicken Stir Fry",
  "Wed": "Vegetable Curry",
  "Thu": "Salad Bowl",
  "Fri": "Chicken Stir Fry",
  "Sat": "Vegetable Curry",
  "Sun": "Omelette"
}
