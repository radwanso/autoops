# Architecture Closure

## Canonical runtime

- Entry point: `autoops.start` launches `autoops.core.engine` and `autoops.web.web`.
- Engine orchestration: `core/pipeline/controller.py`.
- Event transport: singleton in `core/event_bus.py`.
- Handler registration: `core/brain_bus.py` registers brain methods on the singleton.
- State and memory: `core/state_manager.py`, `core/state_schema.py`, `core/memory_store.py`, and `core/memory_engine.py`.
- Recovery: `core/executors/recovery_executor.py`, invoked through policy and decision.
- Dashboard: Flask read APIs and the browser dashboard in `web/`.

## Removed from the release tree

| Removed item | Finding |
|---|---|
| `agent/` and `core/task_queue.py` | The agent was not launched by the canonical runtime and depended on a separate task queue. |
| `legacy/pipeline/` | Historical pipeline implementation with no runtime imports. |
| `core/pipeline/controller.py.bak` | Unused backup of the canonical controller. |
| `actions/fixer.py`, `actions/restart.py`, `actions/task_creator.py`, `actions/escalate.py` | Not part of the verified recovery path; the fixer/task request path had no working consumer. |
| `POST /fix` | Wrote task files that no active worker consumed. The dashboard is read-only in this release. |

The previously delivered v5 archive remains available as a rollback copy.

## Kept capabilities

Service monitoring, event-driven analysis, policy-controlled recovery, narrow non-root systemd restart permissions, JSON state/memory persistence, notifications, and the local dashboard remain in the release.

## Deferred

Manual dashboard recovery, Docker deployment, multi-host monitoring, external databases, and production web serving require a separate concrete requirement and are not blockers for this local release.