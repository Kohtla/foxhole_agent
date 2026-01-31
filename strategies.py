from character_control import move
from foxhole_status import is_foxhole_running
import time

_run_circle_active = False

def start_run_in_circle():
    global _run_circle_active
    _run_circle_active = True
    while _run_circle_active:
        if not is_foxhole_running():
            print("Foxhole is not running. Strategy aborted.")
            time.sleep(1)
            continue
        for direction in ['up', 'left', 'down', 'right']:
            if not _run_circle_active:
                break
            print(f"[RunInCircle] Moving {direction.upper()} for 1s")
            move(direction, 0.5)

def stop_run_in_circle():
    global _run_circle_active
    _run_circle_active = False
