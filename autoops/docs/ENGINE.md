# Engine

## Overview

The Engine is the main runtime loop of AutoOps.

It is responsible for continuously monitoring the system,
executing the processing pipeline,
saving the latest system state,
updating memory,
and coordinating communication between all platform components.

The Engine represents the operational heart of AutoOps.

---

## Responsibilities

The Engine is responsible for:

- Loading configuration
- Reading the current system state
- Loading long-term memory
- Collecting system metrics
- Executing the Pipeline for every configured service
- Saving the updated state
- Publishing system events
- Sending alerts when required
- Running continuously in a controlled loop

---

## Execution Cycle

Each execution cycle performs the following steps:

1. Load configuration.
2. Load current state.
3. Load memory.
4. Collect system metrics.
5. Iterate through every configured service.
6. Execute the Pipeline.
7. Store the updated service state.
8. Publish state updates.
9. Save memory.
10. Wait before the next cycle.

This cycle repeats continuously while AutoOps is running.

---

## Relationship with the Pipeline

The Engine does not contain the intelligence logic itself.

Instead, it delegates service analysis to the Pipeline.

The Pipeline is responsible for reasoning.

The Engine is responsible for orchestration.

---

## Inputs

The Engine consumes:

- Configuration
- Current state
- Memory
- System metrics

---

## Outputs

The Engine produces:

- Updated state
- Updated memory
- Events
- Alerts
- Execution requests

---

## Design Philosophy

The Engine should remain lightweight.

Its responsibility is orchestration rather than decision making.

Business logic should remain inside the specialized engines and the Pipeline.

---

## Current Entry Point

Current production execution starts from:

core/engine.py

This file is the main entry point executed by the AutoOps service.

---

## Notes

The Engine intentionally avoids implementing intelligence algorithms.

Its purpose is to coordinate the platform and maintain the execution lifecycle.
