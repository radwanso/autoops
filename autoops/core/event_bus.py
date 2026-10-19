# autoops/core/event_bus.py

from collections import defaultdict
from typing import Callable, Any


class EventBus:

    def __init__(self):
        self.listeners = defaultdict(list)

    # =========================
    # REGISTER HANDLER
    # =========================
    def on(self, event_name: str, handler: Callable):
        self.listeners[event_name].append(handler)

    # =========================
    # EMIT EVENT
    # =========================
    def emit(self, event_name: str, payload: Any):

        results = []

        if event_name not in self.listeners:
            return results

        for handler in self.listeners[event_name]:

            try:
                result = handler(payload)
                results.append(result)

            except Exception as e:
                print(f"[EVENT ERROR] {event_name}: {e}")

        return results


# GLOBAL INSTANCE
event_bus = EventBus()
