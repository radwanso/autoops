# AutoOps Release Closure

The architecture review and cleanup decisions are complete. The v6 release candidate still needs one short launcher/dashboard smoke check after extraction before creating a GitHub release tag.

## Canonical runtime path

```text
autoops.start
  -> autoops.core.engine
  -> autoops.core.pipeline.controller
  -> core.event_bus + core.brain_bus handler registration
  -> policy and decision
  -> core.executors.recovery_executor
  -> state, memory, event log, and dashboard
```

`event_bus.py` owns the event-bus singleton. `brain_bus.py` registers brain handlers on that singleton; it is bootstrap/registration code, not a second bus.

## Decisions

- Keep the canonical engine, pipeline, state and memory stores, event bus, recovery executor, notifier, configuration, and dashboard.
- Remove the unused agent/task-queue path, abandoned legacy pipeline, pipeline backup, and unconnected action helpers from the release tree.
- Keep dashboard monitoring read-only. The old `/fix` endpoint only wrote task files with no consumer and is not part of this release.
- No speculative features are required for closure.
