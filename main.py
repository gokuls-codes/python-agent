import os
import sys
import argparse
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError

import prompts
from functions.call_function import available_functions, call_function

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

DEFAULT_MODEL = "gemini-3.1-flash-lite-preview"

def run_agent(agent_name, system_prompt, user_content, verbose=False):
    print(f"\n--- Running {agent_name} Agent ---")
    messages = [types.Content(role="user", parts=[types.Part(text=user_content)])]
    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    )

    for _ in range(40):
        # Retry loop for API calls (handle 503 errors)
        max_retries = 5
        response = None
        for retry_attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=DEFAULT_MODEL,
                    contents=messages,
                    config=config
                )
                break
            except ServerError as e:
                # 503 errors are ServerErrors in genai library
                if retry_attempt < max_retries - 1:
                    wait_time = (2 ** retry_attempt)
                    print(f"API Error (503): {e.message}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"Error: API unavailable after {max_retries} retries.")
                    return None
            except Exception as e:
                print(f"Unexpected error: {e}")
                return None

        if not response:
            return None

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose)
                messages.append(function_call_result)
        else:
            print(f"{agent_name} response: {response.text}")
            return response.text

    print(f"Error: {agent_name} reached maximum iterations.")
    return None

# Architect writes todo.md
architect_response = run_agent("Architect", prompts.architect_system_prompt, args.user_prompt, args.verbose)

if architect_response:
    # Coder reads todo.md and acts on it
    coder_response = run_agent("Coder", prompts.coder_system_prompt, "Please read todo.md and complete the task.", args.verbose)



