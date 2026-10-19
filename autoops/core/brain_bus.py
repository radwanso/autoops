# autoops/core/brain_bus.py

from autoops.core.event_bus import event_bus

# IMPORT ALL HANDLERS (IMPORTANT)
from autoops.core.brain import brain  # هذا مهم جداً

from autoops.core.memory_engine import memory_update_handler
from autoops.core.prediction_engine import prediction_failure_handler
from autoops.core.executors.recovery_executor import execute_recovery

# =========================
# REGISTER EVENTS
# =========================

event_bus.on("risk.calculate", brain.calculate_risk)
event_bus.on("mode.calculate", brain.calculate_mode)
event_bus.on("behavior.evaluate", brain.evaluate_behavior)
event_bus.on("incident.classify", brain.classify_incident)

event_bus.on("reputation.calculate", brain.calculate_reputation)
event_bus.on("experience.evaluate", brain.evaluate_experience)

event_bus.on("event.analyze", brain.analyze_events)

event_bus.on(
    "profile.adapt",
    brain.adapt_profile
)

event_bus.on("strategy.choose", brain.choose_strategy)
event_bus.on("decision.make", brain.decide)

event_bus.on(
    "policy.evaluate",
    brain.evaluate_policy
    )
event_bus.on(
    "intent.classify",
    brain.classify_intent
    )

event_bus.on(
    "response.build",
    brain.build_response_plan
    )
event_bus.on(
    "cognitive.build",
    brain.build_cognitive_state
    )

event_bus.on(
    "memory.update",
    memory_update_handler
    )
event_bus.on(
    "recovery.policy",
    brain.build_recovery_policy
    )
event_bus.on(
    "recovery.analyze",
    brain.analyze_recovery_result
    )

event_bus.on(
    "prediction.failure",
    prediction_failure_handler
    )

event_bus.on(
    "state.updated",
    brain.push_state_update
    )

event_bus.on(
    "execution.run",
    execute_recovery
)


event_bus.on("state.push", brain.push_state_update)

