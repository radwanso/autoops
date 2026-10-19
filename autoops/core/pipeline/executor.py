# autoops/core/pipeline/executor.py

from autoops.core.event_bus import event_bus


def safe_emit(bus, event_name, payload, default=None):
    """
    Safe event emission for pipeline execution layer
    """
    try:
        result = bus.emit(event_name, payload)

        if not result:
            return default

        # always return first result (pipeline convention)
        return result[0]

    except Exception:
        return default
