# AutoOps Components

## Active runtime

- `core/engine.py`: periodic service monitoring and runtime coordination.
- `core/pipeline/controller.py`: analysis, policy, decision, and execution orchestration.
- `core/event_bus.py`: singleton event bus.
- `core/brain_bus.py` and `core/brain.py`: handler registration and analysis methods.
- `core/monitor.py`, `core/system_metrics.py`: system and service observation.
- `core/policy.py`, `core/decision.py`, `core/recovery_policy.py`: recovery eligibility and decision.
- `core/executors/recovery_executor.py`: approved systemd restart operation.
- `core/state_manager.py`, `core/state_schema.py`, `core/memory_store.py`, `core/memory_engine.py`: local persistence and normalization.
- `utils/event_logger.py`: event persistence used by runtime and dashboard.
- `web/`: local read-only Flask dashboard and API.
- `actions/notifier.py`: optional Telegram notification support.

See [`ARCHITECTURE_CLEANUP.md`](ARCHITECTURE_CLEANUP.md) for items excluded from this release.