import os
import sys
import argparse
import ollama
import json
from dotenv import load_dotenv

import prompts
from functions.call_function import call_function, get_ollama_tools

load_dotenv()

# The model specified by the user
OLLAMA_MODEL = "qwen3.5:4b-q4_K_M"

parser = argparse.ArgumentParser(description="Ollama Chatbot Agent")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
parser.add_argument("--model", type=str, default=OLLAMA_MODEL, help="Ollama model to use")
args = parser.parse_args()

messages = [
    {'role': 'system', 'content': prompts.system_prompt},
    {'role': 'user', 'content': args.user_prompt}
]

tools = get_ollama_tools()

for _ in range(40):
    if args.verbose:
        print(f"--- Sending request to Ollama ({args.model}) ---")
        
    response = ollama.chat(
        model=args.model,
        messages=messages,
        tools=tools,
    )

    message = response['message']
    messages.append(message)

    # Log what the model is thinking/saying
    if message.get('content'):
        print(f"\n[Model]: {message['content']}")

    # If the model didn't call any tools, we've reached the final answer
    if not message.get('tool_calls'):
        if not message.get('content'):
            print("\n[Done]: Final response received.")
        break

    # If the model called tools, handle them
    if message.get('tool_calls'):
        for tool in message['tool_calls']:
            function_name = tool['function']['name']
            function_args = tool['function']['arguments']
            
            # Ensure function_args is a dict if it's returned as a JSON string
            if isinstance(function_args, str):
                try:
                    function_args = json.loads(function_args)
                except:
                    pass
            
            print(f" - [Action]: Calling {function_name}({json.dumps(function_args)})")
            result = call_function(function_name, function_args, args.verbose)
            
            result_text = str(result.get('result') or result.get('error'))
            # Print a snippet of the result to keep the user informed
            snippet = (result_text[:100] + '...') if len(result_text) > 100 else result_text
            print(f" - [Result]: {snippet}")
            
            # Use 'tool' role with function result
            messages.append({
                'role': 'tool',
                'tool_call_id': tool.get('id'),
                'name': function_name,
                'content': result_text,
            })
else:
    print("Error: Maximum number of iterations reached without a final response.")
    sys.exit(1)

