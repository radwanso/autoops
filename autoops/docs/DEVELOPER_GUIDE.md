# AutoOps Developer Guide

## Purpose

This guide explains how developers should work on AutoOps and how the project is organized.

It is intended for anyone contributing to the platform.

---

## Project Philosophy

AutoOps is designed as a modular platform.

Each component should have a single responsibility.

Communication between modules should occur through well-defined interfaces and the Event Bus whenever possible.

Avoid creating direct dependencies between unrelated modules.

---

## Development Principles

Prefer simple solutions.

Keep components loosely coupled.

Avoid duplicate logic.

Use existing engines before introducing new ones.

Document every architectural change.

Keep functions focused on a single task.

---

## Project Workflow

Typical execution flow:

Configuration

↓

Engine

↓

Pipeline

↓

Brain

↓

Decision

↓

Execution

↓

Memory

↓

State

↓

Dashboard

---

## Adding a New Engine

When introducing a new engine:

Create the module inside:

autoops/core/

Register the engine inside:

brain.py

If the engine is event-driven, register it in:

brain_bus.py

Return structured data instead of printing output.

Document the engine inside docs/.

---

## Adding New Events

Register every new event in:

brain_bus.py

Avoid emitting anonymous events.

Use descriptive event names.

Example:

risk.calculate

memory.update

execution.run

---

## Working With State

Never modify state objects arbitrarily.

Use the normalized state structure.

Missing fields should use default values.

State should remain serializable.

---

## Working With Memory

Memory represents historical knowledge.

Memory should only store long-term information.

Temporary runtime values belong in State.

---

## Logging

Use structured logging whenever possible.

Avoid print() for production features.

Important events should be stored in events.json.

---

## Error Handling

Never allow a component failure to stop the engine.

Catch exceptions.

Return safe defaults.

Log failures.

Continue execution whenever possible.

---

## Documentation

Every architectural change should update:

ARCHITECTURE.md

COMPONENTS.md

DATA_FLOW.md

PROJECT_STATUS.md (if applicable)

---

## Future Contributions

Future development should focus on:

Improving reliability

Simplifying architecture

Reducing technical debt

Enhancing modularity

Preparing production deployment

