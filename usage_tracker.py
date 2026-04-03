import time
from functools import wraps
from logger import agent_logger

# Approximate pricing for Gemini 1.5 Flash (per 1M tokens)
PRICING = {
    "prompt": 0.075,  # $0.075 / 1M 
    "candidate": 0.30, # $0.30 / 1M
}

class TokenTracker:
    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_candidate_tokens = 0
        self.total_cost = 0.0
        self.session_start = time.time()

    def update(self, prompt_tokens, candidate_tokens):
        self.total_prompt_tokens += prompt_tokens
        self.total_candidate_tokens += candidate_tokens
        
        cost = (prompt_tokens / 1_000_000 * PRICING["prompt"]) + \
               (candidate_tokens / 1_000_000 * PRICING["candidate"])
        self.total_cost += cost
        
        return cost

    def get_summary(self):
        duration = time.time() - self.session_start
        return {
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_candidate_tokens": self.total_candidate_tokens,
            "total_tokens": self.total_prompt_tokens + self.total_candidate_tokens,
            "estimated_cost_usd": round(self.total_cost, 6),
            "session_duration_sec": round(duration, 2)
        }

# Global singleton for the session
tracker = TokenTracker()

def track_usage(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        
        if hasattr(response, 'usage_metadata') and response.usage_metadata:
            usage = response.usage_metadata
            p_tokens = usage.prompt_token_count
            c_tokens = usage.candidates_token_count
            
            cost = tracker.update(p_tokens, c_tokens)
            
            # Log individual request usage
            agent_logger.info("Token Usage", extra={
                "request_prompt_tokens": p_tokens,
                "request_candidates_tokens": c_tokens,
                "request_cost_usd": round(cost, 6),
                "cumulative_cost_usd": round(tracker.total_cost, 6)
            })
            
            # Context tracking: log number of messages in the conversation
            if 'contents' in kwargs:
                msg_count = len(kwargs['contents'])
                agent_logger.info("Context Stats", extra={
                    "message_count": msg_count,
                    "estimated_context_depth": msg_count
                })
                
        return response
    return wrapper
