import logging
import json
import datetime
import sys

class JsonFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings for each log record.
    """
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        
        # Include extra data if it exists
        if hasattr(record, 'extra'):
            log_record.update(record.extra)
            
        # Add exception info if present
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_record)

def setup_logger(name="python-agent", level=logging.INFO):
    """
    Configures the logger to output JSON to stdout.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers if setup_logger is called multiple times
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = JsonFormatter(datefmt="%Y-%m-%dT%H:%M:%SZ")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

# Singleton instance for the agent
agent_logger = setup_logger()
