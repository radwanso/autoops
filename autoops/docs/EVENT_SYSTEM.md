# EVENT SYSTEM

## Overview

AutoOps uses an internal Event Bus to decouple system components.

Instead of directly calling modules, the pipeline emits events.

Each event is handled by one or more registered handlers.

This architecture allows components to remain independent while cooperating through a common communication layer.

---

## Event Bus

The Event Bus is implemented in:

```
autoops/core/event_bus.py
```

It provides two core operations:

- Register an event handler.
- Emit an event.

---

## Registering Events

Handlers are registered during system startup.

Registration is performed in:

```
autoops/core/brain_bus.py
```

Example:

event_bus.on("risk.calculate", brain.calculate_risk)

This connects the event:

```
risk.calculate
```

to the function:

```
brain.calculate_risk()
```

---

## Event Execution

When the pipeline emits an event:

↓

The Event Bus searches all registered listeners.

↓

Each listener receives the payload.

↓

The returned value is collected.

↓

The Pipeline continues with the returned result.

This mechanism keeps the Pipeline independent from implementation details.

---

## Safe Execution

The pipeline never calls EventBus.emit() directly.

Instead it uses:

```
safe_emit()
```

located in:

```
pipeline/executor.py
```

safe_emit() guarantees:

- exception handling

- default fallback values

- pipeline continuity

If a handler crashes, the pipeline continues using the supplied default value.

---

## Registered Events

Current events include:

mode.calculate

behavior.evaluate

incident.classify

reputation.calculate

experience.evaluate

event.analyze

prediction.failure

risk.calculate

strategy.choose

recovery.policy

policy.evaluate

intent.classify

response.build

profile.adapt

cognitive.build

decision.make

execution.run

memory.update

state.updated

state.push

---

## Event Categories

### Intelligence

Responsible for analysing the current service state.

Examples:

- behavior.evaluate

- risk.calculate

- prediction.failure

- incident.classify

---

### Decision

Responsible for selecting the next action.

Examples:

- strategy.choose

- decision.make

- policy.evaluate

---

### Execution

Responsible for performing recovery actions.

Examples:

- execution.run

- recovery.policy

- recovery.analyze

---

### Memory

Responsible for updating long-term knowledge.

Example:

memory.update

---

### State Distribution

Responsible for publishing new system state.

Examples:

state.updated

state.push

---

## Event Payload

Each event receives a payload object.

The payload depends on the event type.

Examples:

State object

Memory object

History list

Execution result

Metrics

Configuration

No global variables are required.

---

## Advantages

The Event Bus provides:

- Loose coupling

- Easy module replacement

- Simple testing

- Better scalability

- Clear execution flow

---

## Current Design

The current implementation supports synchronous event execution.

Handlers execute sequentially.

No asynchronous processing is currently implemented.

---

## Future Extensions

The current design allows future support for:

- Multiple handlers per event

- Async execution

- Distributed workers

- External plugins

without changing the Pipeline architecture.
