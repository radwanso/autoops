# AutoOps Data Flow

1. `autoops.core.engine` loads service configuration and current persisted state.
2. The pipeline controller obtains service status and metrics, then runs analysis and policy/decision handlers through the shared event bus.
3. If policy permits recovery, the recovery executor requests a systemd restart for the configured unit.
4. The engine persists state and memory and records events for the dashboard.
5. The dashboard reads state and event JSON and refreshes its display through `/api/state` and `/api/events`.

The dashboard does not create tasks or initiate recovery. See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the component map.