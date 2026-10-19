# Pipeline Controller

## Overview

The Pipeline Controller coordinates the complete processing lifecycle of a service.

For every monitoring cycle, each configured service passes through the Pipeline exactly once.

The Pipeline transforms raw service information into an intelligent decision by executing multiple processing stages in a predefined order.

It is the central orchestration component of the AutoOps intelligence system.

---

## Responsibilities

The Pipeline is responsible for:

- Normalizing the current service state
- Collecting runtime information
- Executing every intelligence module
- Building the cognitive state
- Producing the final decision
- Executing the selected action
- Updating long-term memory
- Returning the final service state

---

## Processing Flow

Each service follows the same sequence.

```
Current State
      │
      ▼
Normalize State
      │
      ▼
Behavior Analysis
      │
      ▼
Incident Classification
      │
      ▼
Reputation Evaluation
      │
      ▼
Experience Evaluation
      │
      ▼
Event Analysis
      │
      ▼
Failure Prediction
      │
      ▼
Risk Calculation
      │
      ▼
Strategy Selection
      │
      ▼
Recovery Policy
      │
      ▼
Policy Evaluation
      │
      ▼
Intent Classification
      │
      ▼
Response Planning
      │
      ▼
Profile Adaptation
      │
      ▼
Cognitive State
      │
      ▼
Decision Making
      │
      ▼
Execution
      │
      ▼
Memory Update
      │
      ▼
Return Final State
```

---

## Event-Driven Architecture

The Pipeline does not directly call most intelligence modules.

Instead, it communicates through the Event Bus.

Each stage emits an event.

Registered handlers perform the required work and return the result.

This keeps components loosely coupled.

---

## State Evolution

The service state grows during execution.

Initially it contains only basic monitoring information.

After each processing stage, new information is added.

For example:

Initial State

- service
- status

After Analysis

- behavior
- incident
- prediction

After Intelligence

- risk
- strategy
- policy
- intent

After Decision

- decision
- execution_result

Final State

- updated memory
- complete service context

---

## Why This Design

Instead of creating one very large function containing all logic, the Pipeline separates every responsibility into independent stages.

Advantages include:

- Easier maintenance
- Easier testing
- Better extensibility
- Independent intelligence modules
- Reduced coupling

---

## Inputs

The Pipeline receives:

- Service configuration
- Current state
- Memory
- System metrics

---

## Outputs

The Pipeline returns:

- Updated service state
- Selected decision
- Execution result
- Updated memory

---

## Notes

The Pipeline should remain an orchestration layer.

Business logic belongs inside the specialized engines.

Whenever possible, new intelligence should be implemented as new Event Bus handlers rather than expanding the Pipeline itself.
