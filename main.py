import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

import prompts
from functions.call_function import available_functions, call_function

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=prompts.system_prompt
        )

for _ in range(40):
    response = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents=messages,
        config=config
        )

    # print("candidates length: ", len(response.candidates))
    if response.candidates and len(response.candidates) > 0:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if response.function_calls and len(response.function_calls) > 0:
        for function_call in response.function_calls:
            # print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call, args.verbose)

            if len(function_call_result.parts) == 0:
                raise Exception("Function call result is empty")

            if not function_call_result.parts[0].function_response:
                raise Exception("Function call result is missing function_response")

            if not function_call_result.parts[0].function_response.response:
                raise Exception("Function call result is missing response")

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

            messages.append(function_call_result)
            # print(messages)
    else:
        print(response.text)
        break

    if response.usage_metadata is not None and args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
else:
    print("Error: Maximum number of iterations reached without a final response.")
    sys.exit(1)

