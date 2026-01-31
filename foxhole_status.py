import psutil
import time
from typing import Callable

GAME_PROCESS_NAMES = ["Foxhole.exe", "War-Win64-Shipping.exe", "War.exe", "War-Win64-Shipping", "War"]

def is_foxhole_running() -> bool:
    """Check if Foxhole is running (by process name)."""
    for proc in psutil.process_iter(['name']):
        name = proc.info['name']
        if name and any(name.lower() == pname.lower() for pname in GAME_PROCESS_NAMES):
            return True
    return False

def watch_foxhole_status(callback: Callable[[bool], None], interval: float = 1.0):
    """Call callback with running status every interval seconds."""
    last_status = None
    while True:
        status = is_foxhole_running()
        if status != last_status:
            callback(status)
            last_status = status
        time.sleep(interval)
