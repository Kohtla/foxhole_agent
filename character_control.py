import keyboard
import time

KEYS = {
    'up': 'w',
    'left': 'a',
    'down': 's',
    'right': 'd',
}

def move(direction: str, duration: float = 1.0):
    """Hold movement key for duration seconds using keyboard module."""
    key = KEYS.get(direction)
    if key:
        keyboard.press(key)
        time.sleep(duration)
        keyboard.release(key)
    else:
        raise ValueError(f"Unknown direction: {direction}")
