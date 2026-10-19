import time
import traceback
import signal
import sys

from autoops.core.pipeline.controller import pipeline
from autoops.core.state_manager import get_state, update_state
from autoops.core.memory_store import load_memory, save_memory
from autoops.core.config import load_config
from autoops.utils.event_logger import log_event
from autoops.actions.notifier import send_telegram
from autoops.core.system_metrics import collect_system_metrics
from autoops.core.brain_bus import event_bus
from autoops.core.monitor import is_service_running


# =========================
# GLOBAL STATE (SAFE)
# =========================
last_service_state = {}
last_alert_time = {}

_last_run = 0
MIN_INTERVAL = 5
ALERT_COOLDOWN = 60


# =========================
# UTILS
# =========================
def safe(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        print(f"[ENGINE ERROR] {fn.__name__}: {e}")
        traceback.print_exc()
        return None


# =========================
# CORE ENGINE
# =========================
def analyze_and_act():
    global _last_run
    global last_service_state
    global last_alert_time

    now = time.time()

    # =========================
    # THROTTLE
    # =========================
    if now - _last_run < MIN_INTERVAL:
        return

    _last_run = now

    print("[ENGINE] tick")

    config = load_config()
    state = get_state()
    memory = load_memory()
    metrics = collect_system_metrics()

    new_state = {}

    for service in config["services"]:
        name = service["name"]

        # =========================
        # SERVICE STATUS
        # =========================
        running = is_service_running(name)
        current_state = "UP" if running else "DOWN"

        # =========================
        # STATE TRACKING (FIXED)
        # =========================
        prev_state = last_service_state.get(name)

        if prev_state is None:
            prev_state = current_state

        state_changed = (prev_state != current_state)
        last_service_state[name] = current_state

        if state_changed:
            log_event(
                "service.state_change",
                {
                    "service": name,
                    "from": prev_state,
                    "to": current_state
                }
            )

        # =========================
        # PIPELINE EXECUTION
        # =========================
        result_obj = pipeline.run(
            name,
            service,
            state.get(name, {}),
            memory,
            metrics
        )

        service_state_obj = result_obj["state"]
        decision = result_obj["decision"]

        risk_obj = service_state_obj.get("risk", {})

        if isinstance(risk_obj, dict):
            risk = risk_obj.get("level", "LOW")
        else:
            risk = str(risk_obj or "LOW")

        log_event(
            "service.evaluate",
            {
                "service": name,
                "status": current_state,
                "risk": risk,
                "decision": decision
            }
        )

        # =========================

        # ALERT CONTROL (FIXED + SAFE)
        # =========================
        alert_key = f"{name}:{risk}:{running}"

        last_time = last_alert_time.get(alert_key, 0)

        if risk in ["HIGH", "CRITICAL"]:

            if now - last_time >= ALERT_COOLDOWN:

                last_alert_time[alert_key] = now

                send_telegram(
                    f"🚨 ALERT: {name} | risk={risk} | running={running}"
                )

        elif risk == "LOW":
            # optional: no spam stable messages
            pass

        # =========================
        # PERSIST FULL PIPELINE STATE
        # =========================
        service_state_obj["service"] = name
        service_state_obj["status"] = current_state
        service_state_obj["running"] = running
        service_state_obj["decision"] = decision

        new_state[name] = service_state_obj


    # =========================
    # GLOBAL STATE SAVE
    # =========================
    update_state(new_state)
    event_bus.emit("state.updated", new_state)
    save_memory(memory)


# =========================
# MAIN LOOP (STABLE)
# =========================
def main():
    print("BRAIN ENGINE v3 (PRODUCTION STABLE MODE)")

    def shutdown_handler(signum, frame):
        log_event("service.stop", {"status": "stopped"})
        print("[ENGINE] shutting down")
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    while True:
        try:
            analyze_and_act()
            log_event("engine.tick", {"status": "running"})
            time.sleep(5)

        except Exception as e:
            print("[ENGINE CRASH]", e)
            traceback.print_exc()
            log_event("engine.error", {"error": str(e)})
            time.sleep(5)


if __name__ == "__main__":
    main()
