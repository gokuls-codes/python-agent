import logging
import json
import datetime
import sys
import os

class JsonFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings for each log record.
    """
    def format(self, record):
        # Base attributes
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        
        # Standard attributes to exclude from extra
        standard_attrs = {
            'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename', 
            'funcName', 'levelname', 'levelno', 'lineno', 'module', 
            'msecs', 'msg', 'name', 'pathname', 'process', 'processName', 
            'relativeCreated', 'stack_info', 'thread', 'threadName'
        }

        # Include any extra data added via the 'extra' parameter
        for key, value in record.__dict__.items():
            if key not in standard_attrs and not key.startswith('_'):
                log_record[key] = value
                
        # Add exception info if present
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_record)

def setup_logger(name="python-agent", level=logging.INFO):
    """
    Configures the logger to output JSON to both stdout and a session file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Ensure .sessions directory exists
    sessions_dir = ".sessions"
    os.makedirs(sessions_dir, exist_ok=True)
    
    # Generate session ID based on timestamp
    session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(sessions_dir, f"session_{session_id}.log")

    # Avoid duplicate handlers if setup_logger is called multiple times
    if not logger.handlers:
        # 1. Console Handler (Standard Out)
        console_handler = logging.StreamHandler(sys.stdout)
        formatter = JsonFormatter(datefmt="%Y-%m-%dT%H:%M:%SZ")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # 2. File Handler (Persistent Log)
        file_handler = logging.FileHandler(log_filename)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        logger.info(f"Logging initialized. Session ID: {session_id}", extra={"log_file": log_filename})
        
    return logger

# Singleton instance for the agent
agent_logger = setup_logger()
