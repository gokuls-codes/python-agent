import os

HISTORY_FILE = "history.txt"

def save_to_history(expression):
    with open(HISTORY_FILE, "a") as f:
        f.write(expression + "\n")

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]
