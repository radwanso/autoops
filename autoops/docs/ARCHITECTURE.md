# AutoOps Architecture

## Runtime path

```text
autoops.start
  +-- autoops.core.engine
  |     -> core.pipeline.controller
  |     -> policy and decision
  |     -> core.executors.recovery_executor
  |     -> systemd service state
  |
  +-- autoops.web.web
        -> read-only dashboard and monitoring API
```

`core.event_bus` provides one event-bus singleton. Importing `core.brain_bus` registers brain handlers on it. The pipeline uses that same bus.

## Persistent data

State, memory, and events are stored as local JSON files under `autoops/data/`. Runtime data is generated on the host and excluded from the source repository.

## Scope

This release supports one Linux systemd host and a local Flask dashboard. Recovery is performed by the engine under configured policy. See [`PROJECT_STATUS.md`](../PROJECT_STATUS.md) and [`ARCHITECTURE_CLEANUP.md`](ARCHITECTURE_CLEANUP.md) for verified behavior and exclusions.