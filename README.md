# SmartMeal — AI Meal Planner & Smart Shopping Agent

**Track:** Concierge Agents (Kaggle Agents Intensive)

This repository implements a multi-agent system that:
1. Understands user preferences (Input agent)
2. Plans a 7-day menu (Meal Planner)
3. Extracts ingredients into a shopping list (Shopping List agent)
4. Estimates prices & suggests substitutions (Price Optimizer)
5. Validates and auto-fixes problems (Validation agent)
6. Persists preferences/history (Memory agent)

The system runs in **fallback mode (no API keys required)** and supports **LLM-enhanced mode** when `OPENAI_API_KEY` is provided (via environment variable / GitHub Codespaces secret).

---

## Quick start (local)

```bash
# clone repo (if not already)
git clone https://github.com/<your-username>/meal-planner-smart-shopping-agent.git
cd meal-planner-smart-shopping-agent

# create virtual env and install
python3 -m venv venv
source venv/bin/activate   # Windows: .\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

# run fallback demo
python main.py
