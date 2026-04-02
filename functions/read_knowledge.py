import json
import os

schema_read_knowledge = {
    "name": "read_knowledge",
    "description": "Read the shared knowledge base to understand context, discovered facts, or rules from other agents.",
    "parameters": {
        "type": "object",
        "properties": {}
    }
}

def read_knowledge(**kwargs):
    knowledge_path = os.path.join(kwargs.get("working_directory", "."), "knowledge.json")
    if not os.path.exists(knowledge_path):
        return "Knowledge base is currently empty."
    
    try:
        with open(knowledge_path, "r") as f:
            data = json.load(f)
            return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error reading knowledge: {str(e)}"
