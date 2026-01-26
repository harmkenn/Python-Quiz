# state.py
import threading
import time


class BuzzState:
    def __init__(self):
        self.lock = threading.Lock()
        self.first_buzz = None  # {"team": str, "timestamp": float}
        self.last_clear = time.time()

    def buzz(self, team_name: str):
        """Attempt to buzz in. Returns (success: bool, first_buzz: dict|None)."""
        now = time.time()
        with self.lock:
            if self.first_buzz is None:
                self.first_buzz = {"team": team_name, "timestamp": now}
                return True, self.first_buzz
            else:
                return False, self.first_buzz

    def clear(self):
        with self.lock:
            self.first_buzz = None
            self.last_clear = time.time()

    def get(self):
        with self.lock:
            return self.first_buzz
        

BUZZ_STATE = BuzzState()
