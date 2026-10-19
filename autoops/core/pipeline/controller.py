import time
import autoops.core.brain_bus
from autoops.core.event_bus import event_bus
from autoops.core.system_metrics import collect_system_metrics
from autoops.core.pipeline.executor import safe_emit
from autoops.core.state_schema import normalize_state


class PipelineController:




    def collect_system_metrics(self):
        return collect_system_metrics()

    def run(self, service_name, service_config, state, memory, metrics):

        # =========================
        # SAFE STATE
        # =========================
        state = normalize_state(state, service_name)
        state["metrics"] = metrics
        # =========================
        # SERVICE STATUS
        # =========================

        from autoops.core.monitor import is_service_running

        running = is_service_running(service_name)

        previous_status = state.get("status", "UP")
        current_status = "UP" if running else "DOWN"

        state["running"] = running
        state["status"] = current_status

        # Count only a new failure transition
        if current_status == "DOWN" and previous_status != "DOWN":
            state["fail_count"] += 1
            state["last_failure_time"] = time.time()

            state.setdefault("history", []).append({
                "time": time.time(),
                "event": "DOWN",
                "service": service_name
            })

        elif current_status == "UP" and previous_status == "DOWN":
            # A monitored return to UP closes the current failure streak. Keep
            # the event history for diagnostics, but do not let old outages
            # permanently disable future recovery.
            state["fail_count"] = 0
            state["restart_attempts"] = 0
            state["success_count"] += 1
            state["last_fix_time"] = time.time()
            state.setdefault("history", []).append({
                "time": time.time(),
                "event": "SUCCESS",
                "service": service_name
            })

        # Keep history bounded
        state["history"] = state.get("history", [])[-50:]

        history = state.get("history", [])

        mem = memory.get(service_name, {})

        # =========================
        # EVENT PIPELINE (SAFE MODE)
        # =========================

        state["mode"] = safe_emit(event_bus, "mode.calculate", state, "NORMAL")

        state["incident"] = safe_emit(event_bus, "incident.classify", state, {})

        state["reputation"] = safe_emit(
            event_bus,
            "reputation.calculate",
            mem,
            1.0
        )

        state["experience"] = safe_emit(
            event_bus,
            "experience.evaluate",
            mem,
            {}
        )

        state["event_analysis"] = safe_emit(
            event_bus,
            "event.analyze",
            history,
            []
        )

        state["profile"] = safe_emit(
            event_bus,
            "profile.adapt",
            {
                "profile": service_config.get("profile", {}),
                "events": state.get("event_analysis", {}),
                "risk": state.get("risk", {})
            },
            service_config.get("profile", {})
        )

        state["behavior"] = safe_emit(
            event_bus,
            "behavior.evaluate",
            state,
            {}
        )


        state["prediction"] = safe_emit(
            event_bus,
            "prediction.failure",
            {
                "events": state["event_analysis"],
                "reputation": state["reputation"]
            },
            {
                "will_fail": False,
                "confidence": 0
            }
        )

        state["risk"] = safe_emit(
            event_bus,
            "risk.calculate",
            state,
            {"level": "LOW"}
        )

        state["strategy"] = safe_emit(
            event_bus,
            "strategy.choose",
            state,
            "OBSERVE"
        )

        state["recovery_policy"] = safe_emit(
            event_bus,
            "recovery.policy",
            state,
            {}
        )

        state["policy"] = safe_emit(
            event_bus,
            "policy.evaluate",
            state,
            {
                "safe_mode": False,
                "allow_restart": True
            }
        )

        state["intent"] = safe_emit(
            event_bus,
            "intent.classify",
            state,
            "UNKNOWN"
        )

        state["response_plan"] = safe_emit(
            event_bus,
            "response.build",
            state,
            {}
        )


        state["service"] = service_name


        state["cognitive_state"] = safe_emit(
            event_bus,
            "cognitive.build",
            state,
            {}
        )

        # =========================
        # DECISION LAYER
        # =========================

        decision = safe_emit(
            event_bus,
           "decision.make",
           state,
           "OBSERVE"
        )

        # =========================
        # EXECUTION LAYER
        # =========================

        result = safe_emit(
            event_bus,
            "execution.run",
            {
                "state": state,
                "decision": decision
            },
            {
                "status": "SKIPPED"
            }
        )

        if (
            isinstance(result, dict)
            and result.get("status") in {"RESTART_SENT", "FAILED"}
            and decision in {"RESTART", "RECOVER"}
        ):
            # Count actual restart commands, not outage detections. This is
            # the safety limit used to stop repeated failed recovery loops.
            state["restart_attempts"] += 1
            state.setdefault("history", []).append({
                "time": time.time(),
                "event": "RESTART",
                "service": service_name
            })

        print(
            "[EXECUTION]",
            service_name,
            decision,
            result
        )
        # =========================
        # MEMORY UPDATE
        # =========================

        memory = safe_emit(
            event_bus,
            "memory.update",
            {
                "memory": memory,
                "state": state
            },
            memory
        )

        # =========================
        # RETURN FINAL STATE
        # =========================

        return {
            "state": state,
            "decision": decision,
            "result": result,
            "memory": memory
        }

# ====================================
# GLOBAL SINGLETON
# ====================================

pipeline = PipelineController()
