import os
import sys
import argparse
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError

import prompts
from functions.call_function import architect_tools, coder_tools, qa_tools, call_function
from logger import agent_logger
from usage_tracker import track_usage, tracker
from guardrails import check_prompt

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

DEFAULT_MODEL = "gemini-3.1-flash-lite-preview"

AGENT_CONFIGS = {
    "Architect": {"prompt": prompts.architect_system_prompt, "tools": architect_tools},
    "Coder": {"prompt": prompts.coder_system_prompt, "tools": coder_tools},
    "QA": {"prompt": prompts.qa_system_prompt, "tools": qa_tools}
}

MAX_HANDOFFS = 10
MAX_AGENT_ITERATIONS = 40

def run_agent(agent_name, user_content, verbose=False):
    agent_logger.info(f"Running agent: {agent_name}", extra={"agent_name": agent_name})
    config_entry = AGENT_CONFIGS.get(agent_name)
    if not config_entry:
        agent_logger.error(f"Unknown agent: {agent_name}", extra={"agent_name": agent_name})
        return None

    messages = [types.Content(role="user", parts=[types.Part(text=user_content)])]
    config = types.GenerateContentConfig(
        tools=[config_entry["tools"]],
        system_instruction=config_entry["prompt"]
    )

    for iteration in range(MAX_AGENT_ITERATIONS):
        # Retry loop for API calls (handle 503 errors)
        max_retries = 5
        response = None
        for retry_attempt in range(max_retries):
            try:
                # Local wrapper to enable decorator to work correctly
                @track_usage
                def call_model():
                    return client.models.generate_content(
                        model=DEFAULT_MODEL,
                        contents=messages,
                        config=config
                    )
                
                response = call_model()
                break
            except ServerError as e:
                if retry_attempt < max_retries - 1:
                    wait_time = (2 ** retry_attempt)
                    agent_logger.warning(f"API Error (503): {e.message}. Retrying in {wait_time}s...", extra={"retry_attempt": retry_attempt, "wait_time": wait_time})
                    time.sleep(wait_time)
                else:
                    agent_logger.error(f"API unavailable after {max_retries} retries.", extra={"error": str(e)})
                    return None
            except Exception as e:
                agent_logger.error(f"Unexpected error calling API: {str(e)}", extra={"error": str(e)})
                return None

        if not response:
            return None

        if response.candidates:
            # We already log usage via the @track_usage decorator
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls:
            for function_call in response.function_calls:
                # Detect handoff
                if function_call.name == "handoff_to_agent":
                    args_dict = dict(function_call.args)
                    target = args_dict.get("target_agent")
                    instruction = args_dict.get("instruction")
                    agent_logger.info(f"Handing off task from {agent_name} to {target}", extra={
                        "from_agent": agent_name,
                        "to_agent": target,
                        "instruction": instruction
                    })
                    # Return special result to trigger next agent in the main loop
                    return {"type": "handoff", "target": target, "instruction": instruction}

                function_call_result = call_function(function_call, verbose)
                messages.append(function_call_result)
        else:
            agent_logger.info(f"{agent_name} completed task", extra={"agent_name": agent_name})
            return {"type": "success", "data": response.text}


    agent_logger.error(f"{agent_name} reached maximum iterations.", extra={"agent_name": agent_name})
    return {"type": "error", "message": f"{agent_name} reached maximum iterations."}


# Start the chain with the Architect
try:
    current_agent = "Architect"
    current_instruction = args.user_prompt
    handoff_count = 0
    final_output = None

    # Step 0: Security Guardrail Check
    is_safe, reason = check_prompt(client, current_instruction)
    if not is_safe:
        agent_logger.error(f"Guardrail Blocked Input: {reason}")
        sys.exit(1)

    while current_agent and handoff_count <= MAX_HANDOFFS:
        agent_logger.info(f"Execution Loop: Agent {current_agent} (Handoff {handoff_count})", extra={
            "agent": current_agent,
            "handoff_count": handoff_count
        })
        
        result = run_agent(current_agent, current_instruction, args.verbose)
        
        if not result or result["type"] == "error":
            agent_logger.error(f"Agent {current_agent} failed.", extra={"result": result})
            break
            
        if result["type"] == "handoff":
            current_agent = result["target"]
            current_instruction = result["instruction"]
            handoff_count += 1
            if handoff_count > MAX_HANDOFFS:
                agent_logger.error("Global Handoff limit reached!", extra={"max_handoffs": MAX_HANDOFFS})
                break
        else:
            # Success
            final_output = result["data"]
            print(f"\nFinal Task Result:\n{final_output}")
            break
finally:
    # Always log the final session summary
    summary = tracker.get_summary()
    summary["total_handoffs"] = handoff_count
    agent_logger.info("Session Summary", extra=summary)





