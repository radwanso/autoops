# AutoOps Project Structure

## Overview

The project is divided into logical components.

---

## actions/

Recovery actions.

Examples:

- restart
- escalation
- notifications

---

## agent/

Legacy execution agent.

Currently inactive.

Scheduled for removal or redesign.

---

## config/

Configuration files.

---

## core/

System intelligence.

Contains:

- Engine
- Pipeline
- Event Bus
- Decision
- Memory
- Prediction
- Risk
- Strategy
- Recovery

---

## data/

Persistent runtime data.

Contains:

- state
- memory
- events
- tasks

---

## docs/

Project documentation.

Represents the official technical reference.

---

## utils/

Logging and utility helpers.

---

## web/

Dashboard and REST API.

---

# Design Principle

Business logic belongs inside **core/**.

Other directories should remain lightweight and specialized.
