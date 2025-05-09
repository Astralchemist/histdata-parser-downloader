# utils.py

import os
from datetime import datetime

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def month_str(month: int) -> str:
    return f"{month:02d}"

def log(message: str):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")
