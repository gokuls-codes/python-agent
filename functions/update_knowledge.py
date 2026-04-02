import json
import os

schema_update_knowledge = {
    "name": "update_knowledge",
    "description": "Update or add a fact to the shared knowledge base for other agents to see.",
    "parameters": {
        "type": "object",
        "properties": {
            "key": {
                "type": "string",
                "description": "The unique name for the fact (e.g. 'db_path' or 'naming_convention')."
            },
            "value": {
                "type": "string",
                "description": "The detailed finding or rule to save."
            }
        },
        "required": ["key", "value"]
    }
}

def update_knowledge(key, value, **kwargs):
    knowledge_path = os.path.join(kwargs.get("working_directory", "."), "knowledge.json")
    
    data = {}
    if os.path.exists(knowledge_path):
        try:
            with open(knowledge_path, "r") as f:
                data = json.load(f)
        except:
            data = {}

    data[key] = value
    
    try:
        with open(knowledge_path, "w") as f:
            json.dump(data, f, indent=2)
        return f"Successfully saved knowledge: {key}."
    except Exception as e:
        return f"Error updating knowledge: {str(e)}"
