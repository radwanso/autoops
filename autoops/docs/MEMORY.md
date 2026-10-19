# AutoOps Memory System

## Overview

The Memory System stores long-term knowledge about every monitored service.

Unlike the runtime state, memory is persistent and survives engine restarts.

Its purpose is to help AutoOps learn from previous incidents and make better future decisions.

---

# Storage

Memory is stored in:

```
autoops/data/memory.json
```

Each monitored service has its own memory section.

Example:

```json
{
    "nginx": {
        "incidents": [],
        "reputation_score": 1.0,
        "total_failures": 0,
        "total_restarts": 0,
        "total_recoveries": 0,
        "risk_history": [],
        "modes": []
    }
}
```

---

# Memory Structure

## incidents

Stores the latest classified incidents.

Purpose:

- historical analysis
- future prediction
- reputation calculation

---

## reputation_score

Represents the overall reliability of the service.

Higher values indicate more stable historical behavior.

Used by:

- Reputation Engine
- Prediction Engine

---

## total_failures

Accumulates detected failures over time.

Updated by:

Memory Engine

---

## total_restarts

Counts all restart attempts performed by AutoOps.

Useful for long-term statistics.

---

## total_recoveries

Counts successful recoveries.

Can later be used to calculate recovery effectiveness.

---

## risk_history

Stores recent calculated risk levels.

Example:

```
LOW
LOW
HIGH
CRITICAL
LOW
```

Only the latest entries are preserved.

---

## modes

Stores operating modes over time.

Example:

```
NORMAL
RECOVERING
UNSTABLE
CRITICAL
```

Used for long-term behavior analysis.

---

# Memory Update Process

After each execution cycle:

```
Pipeline
        ↓
Execution
        ↓
Memory Engine
        ↓
memory.json
```

Memory is updated only after the execution phase has completed.

---

# Memory Engine Responsibilities

The Memory Engine is responsible for:

- updating statistics
- recording incidents
- updating reputation
- storing mode history
- storing risk history

The Memory Engine should never make operational decisions.

---

# Difference Between State and Memory

State represents the current situation.

Memory represents historical knowledge.

State changes every execution cycle.

Memory grows over time.

---

# Future Expansion

The Memory System is designed to support future capabilities, including:

- anomaly detection
- adaptive thresholds
- predictive maintenance
- service learning
- long-term analytics
- AI-assisted recommendations
