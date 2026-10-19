# AutoOps Configuration

## Overview

AutoOps loads its configuration from:

```
autoops/config/config.yaml
```

The configuration defines which services are monitored and how recovery should behave.

---

# Service Configuration

Example:

```yaml
services:
  - name: nginx
    auto_fix: true
```

Each service has its own recovery profile.

---

# Profile

A profile contains service-specific recovery parameters.

Example:

```yaml
profile:

  criticality: high

  restart_threshold: 2

  escalation_threshold: 5

  cooldown: 30

  max_restarts_per_hour: 5
```

---

# Parameters

## criticality

Defines service importance.

Typical values:

- low
- medium
- high

---

## restart_threshold

Number of failures before the service is considered unstable.

---

## escalation_threshold

Maximum allowed failures before escalation.

---

## cooldown

Minimum time between recovery attempts.

---

## max_restarts_per_hour

Upper limit for restart operations.

Prevents restart loops.

---

# Loading

Configuration is loaded through:

```
core/config.py
```

The configuration is loaded during engine startup.

---

# Future Expansion

Possible future configuration options include:

- notification channels
- maintenance windows
- plugin configuration
- remote nodes
- recovery priorities
