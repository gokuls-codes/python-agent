from .get_files_info import schema_get_files_info, get_files_info
from .get_file_content import schema_get_file_content, get_file_content
from .run_python_file import schema_run_python_file, run_python_file
from .write_file import schema_write_file, write_file

available_functions_gemini = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file
]

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file
}

def call_function(function_name, function_args, verbose=False):
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in function_map:
        return {"error": f"Unknown function: {function_name}"}

    args = dict(function_args) if function_args else {}
    args["working_directory"] = "./calculator"

    try:
        function_result = function_map[function_name](**args)
        return {"result": function_result}
    except Exception as e:
        return {"error": str(e)}

def get_ollama_tools():
    """Converts Gemini function declarations to Ollama-compatible tool definitions."""
    tools = []
    for func in available_functions_gemini:
        # Extract properties and types from Gemini types.Schema/FunctionDeclaration
        # Note: In a real scenario, it's better to define schemas as dicts to avoid this.
        # But for now, we'll try to extract what we need.
        params = func.parameters
        properties = {}
        required = []
        
        if params and params.properties:
            for prop_name, prop_schema in params.properties.items():
                properties[prop_name] = {
                    "type": str(prop_schema.type).split(".")[-1].lower(), # Convert Enum to string
                    "description": prop_schema.description
                }
                # Check if property is required
                if params.required and prop_name in params.required:
                    required.append(prop_name)

        tools.append({
            "type": "function",
            "function": {
                "name": func.name,
                "description": func.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        })
    return tools
