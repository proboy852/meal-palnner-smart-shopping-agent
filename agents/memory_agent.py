import json
from pathlib import Path

MEMORY_FILE = Path("memory.json")

class MemoryAgent:
    def load(self):
        if MEMORY_FILE.exists():
            return json.loads(MEMORY_FILE.read_text())
        return {"history": [], "preferences": {"vegetarian": False, "allergies": [], "disliked": [], "budget": "medium"}}

    def save(self, data):
        MEMORY_FILE.write_text(json.dumps(data, indent=2))
