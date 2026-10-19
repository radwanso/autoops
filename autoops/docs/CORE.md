# AutoOps Core

## Overview

The `core` package is the brain of the AutoOps platform.

It contains all decision-making components responsible for monitoring services,
analyzing their behavior, evaluating risk, selecting recovery strategies,
executing actions, and maintaining system memory.

Almost every important operation inside AutoOps passes through this package.

---

## Responsibilities

The core package is responsible for:

- Monitoring system services
- Building the current service state
- Evaluating service behavior
- Detecting incidents
- Calculating operational risk
- Selecting recovery strategies
- Making autonomous decisions
- Executing recovery actions
- Updating long-term memory
- Publishing events across the platform

---

## Internal Architecture

The core package is organized into several logical layers.

### Monitoring Layer

Responsible for collecting information from the operating system.

Main files:

- monitor.py
- system_metrics.py

---

### Analysis Layer

Transforms raw information into structured knowledge.

Main files:

- behavior.py
- classifier.py
- event_intelligence.py
- patterns.py
- mode_engine.py

---

### Intelligence Layer

Produces higher-level reasoning.

Main files:

- reputation_engine.py
- experience_engine.py
- prediction_engine.py
- risk_engine.py
- strategy_engine.py
- policy.py
- intent_engine.py
- cognitive_engine.py

---

### Decision Layer

Produces the final decision for every service.

Main file:

- decision.py

Possible decisions include:

- OBSERVE
- RESTART
- ESCALATE
- STABLE

---

### Execution Layer

Runs the selected action.

Main files:

- execution.py
- executors/
- actions_registry.py

---

### Memory Layer

Stores historical knowledge and updates service memory.

Main files:

- memory_engine.py
- memory_store.py

---

### Pipeline Layer

Coordinates all processing stages.

Main files:

- pipeline/controller.py
- pipeline/executor.py

---

### Event System

Allows components to communicate without direct dependencies.

Main files:

- event_bus.py
- brain_bus.py

---

## Design Philosophy

The AutoOps core follows an event-driven architecture.

Each component has a single responsibility.

Components communicate through the Event Bus instead of directly calling each other whenever possible.

This makes the platform easier to maintain, extend, and test.

---

## Current Entry Point

Current production execution starts from:

core/engine.py

The engine repeatedly executes the Pipeline for every configured service.

---

## Notes

Some files inside the core directory belong to earlier generations of AutoOps.

They remain in the repository for compatibility and future refactoring.

Unused components should eventually be removed after confirming they are no longer referenced.
