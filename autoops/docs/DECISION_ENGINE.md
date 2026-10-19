# AutoOps Decision Engine

## Overview

The Decision Engine is responsible for selecting the final action for every monitored service.

It combines the output of multiple intelligence modules and produces one operational decision.

The Decision Engine never performs actions directly. It only decides what should happen next.

---

# Inputs

The Decision Engine evaluates the current service state, including:

- service status
- operating mode
- behavior analysis
- calculated risk
- recovery policy
- prediction
- reputation
- profile
- historical failures

---

# Decision Flow

```
Current State
        ↓
Behavior
        ↓
Risk
        ↓
Policy
        ↓
Prediction
        ↓
Decision
```

---

# Possible Decisions

## STABLE

The service is healthy.

No action is required.

---

## OBSERVE

The service should continue to be monitored.

No recovery action is performed.

---

## RESTART

The service should be restarted.

Usually selected when:

- restart is allowed
- failure appears recoverable
- policy permits recovery

---

## ESCALATE

Recovery should stop.

The incident requires manual intervention.

Typical reasons include:

- too many failures
- recovery limit exceeded
- recovery considered unsafe
- critical operating mode

---

# Decision Principles

The Decision Engine should:

- avoid unnecessary recovery
- avoid restart loops
- respect recovery policies
- prioritize service stability
- minimize operational risk

---

# Decision Dependencies

The Decision Engine relies on information produced by:

- Mode Engine
- Behavior Engine
- Risk Engine
- Prediction Engine
- Policy Engine
- Recovery Policy
- Reputation Engine

It does not calculate these values itself.

---

# Execution

Once a decision has been selected:

```
Decision
        ↓
Execution Layer
        ↓
Recovery Executor
```

The Decision Engine is not responsible for execution.

---

# Future Expansion

The decision process is designed to support future enhancements, including:

- confidence scoring
- weighted decision models
- machine learning
- adaptive recovery strategies
- user-defined decision policies
