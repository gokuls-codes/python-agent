from google.genai import types
from .get_files_info import schema_get_files_info, get_files_info
from .get_file_content import schema_get_file_content, get_file_content
from .run_python_file import schema_run_python_file, run_python_file_in_docker
from .write_file import schema_write_file, write_file
from .read_knowledge import schema_read_knowledge, read_knowledge
from .update_knowledge import schema_update_knowledge, update_knowledge
from logger import agent_logger

schema_handoff_to_agent = {
    "name": "handoff_to_agent",
    "description": "Hand off the task to another agent. Use 'Coder' after creating todo.md, or 'QA' after the work is done.",
    "parameters": {
        "type": "object",
        "properties": {
            "target_agent": {
                "type": "string",
                "description": "The name of the agent to hand off to (e.g., 'Coder', 'QA')."
            },
            "instruction": {
                "type": "string",
                "description": "The instruction or context for the next agent."
            }
        },
        "required": ["target_agent", "instruction"]
    }
}

def handoff_to_agent(target_agent, instruction, **kwargs):
    return f"Handing off to {target_agent} with instruction: {instruction}"

architect_tools = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_handoff_to_agent,
        schema_read_knowledge,
        schema_update_knowledge
    ]
)

coder_tools = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
        schema_handoff_to_agent,
        schema_read_knowledge,
        schema_update_knowledge
    ]
)

qa_tools = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_handoff_to_agent,
        schema_read_knowledge,
        schema_update_knowledge
    ]
)


function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file_in_docker,
        "write_file": write_file,
        "handoff_to_agent": handoff_to_agent,
        "read_knowledge": read_knowledge,
        "update_knowledge": update_knowledge
        }



def call_function(function_call, verbose=False):
    function_name = function_call.name or ""
    args = dict(function_call.args) if function_call.args else {}
    
    agent_logger.info(f"Calling function: {function_name}", extra={
        "function_name": function_name,
        "function_args": args if verbose else "Redacted (verbose=False)"
    })

    if function_name not in function_map:
        return types.Content(
                role="tool",
                parts=[
                    types.Part(
                        function_response=types.FunctionResponse(
                            id=function_call.id,
                            name=function_name,
                            response={
                                "error": f"Unknown function: {function_name}",
                            }
                        )
                    )
                ]
            )


    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"

    function_result = function_map[function_name](**args)

    return types.Content(
            role="tool",
            parts=[
                types.Part(
                    function_response=types.FunctionResponse(
                        id=function_call.id,
                        name=function_name,
                        response={
                            "result": function_result
                        }
                    )
                )
            ]
        )
