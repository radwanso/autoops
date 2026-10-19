# AutoOps Event System

## Overview

AutoOps uses an Event Bus architecture to decouple system components.

Instead of calling engines directly, the Pipeline emits events and receives the returned results from registered handlers.

This design keeps the system modular and makes it easier to replace or extend components without modifying the Pipeline.

---

# Event Flow

```
Engine
    ↓
Pipeline
    ↓
Event Bus
    ↓
Registered Handler
    ↓
Result
    ↓
Pipeline
```

---

# Event Registration

All event handlers are registered inside:

```
autoops/core/brain_bus.py
```

This file acts as the central registry for the system.

---

# Registered Events

## mode.calculate

Calculates the operating mode of the service.

Returns:

```
NORMAL
RECOVERING
UNSTABLE
CRITICAL
```

---

## behavior.evaluate

Evaluates service behavior.

Returns:

```python
{
    "unstable": bool,
    "safe_to_restart": bool
}
```

---

## incident.classify

Classifies the current incident.

Examples:

- STABLE
- FAILURE
- RECOVERY

---

## reputation.calculate

Calculates the reputation score using historical memory.

---

## experience.evaluate

Evaluates previous recovery experience.

---

## event.analyze

Analyzes historical events.

Used for pattern detection and prediction.

---

## prediction.failure

Predicts future failures.

Returns:

```python
{
    "will_fail": bool,
    "confidence": float
}
```

---

## risk.calculate

Calculates service risk.

Possible values:

- LOW
- HIGH
- CRITICAL

---

## strategy.choose

Chooses the operational strategy.

Examples:

- OBSERVE
- RECOVER
- ESCALATE

---

## recovery.policy

Builds recovery constraints.

Examples:

- restart allowed
- cooldown
- retry limits

---

## policy.evaluate

Evaluates whether recovery actions are currently permitted.

---

## intent.classify

Determines the operational intent.

---

## response.build

Builds the response plan before execution.

---

## profile.adapt

Adapts the service profile according to observed behavior.

---

## cognitive.build

Builds the complete cognitive state used by the decision engine.

---

## decision.make

Produces the final operational decision.

Examples:

- STABLE
- OBSERVE
- RESTART
- ESCALATE

---

## execution.run

Executes the selected recovery action.

Returns execution status.

---

## memory.update

Updates persistent memory after execution.

---

## state.updated

Broadcasts the latest system state.

Currently used for dashboard synchronization.

---

# Event Bus Principles

Every event should:

- receive one payload
- return one result
- avoid modifying unrelated components
- remain independent from the Pipeline

---

# Advantages

The Event Bus provides:

- loose coupling
- modular architecture
- easier testing
- easier maintenance
- plugin-ready architecture
