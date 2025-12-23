# Signal Relay Service

A lightweight signal relay service that decouples **signal generation** and **signal execution**
across multiple trading platforms.

This service is designed to receive trading signals from platforms such as **JoinQuant**
or local research scripts, normalize and persist them, and allow execution engines such as
**QMT** to query and execute signals in a unified and controlled manner.

---

## Core Idea

This service is intentionally **execution-agnostic**.

- Signal producers (e.g. JoinQuant strategies) only **generate signals**
- Signal consumers (e.g. QMT execution engine) only **execute signals**
- This service acts as a **neutral relay layer** in between

```
JoinQuant / Local Strategy
            ↓
     Signal Relay Service
            ↓
              QMT
```

---

## Signal Model

Each trading signal is explicitly described using the following dimensions:

| Field              | Description |
|-------------------|-------------|
| `source_platform` | Signal source platform (e.g. `joinquant`, `local`) |
| `source_strategy` | Strategy identifier within the source platform |
| `signal_type`     | Trading intent (e.g. `open`, `close`, `rebalance`) |
| `symbol`          | Target instrument code (e.g. `000001.SZ`) |
| `target_position` | Target position ratio (e.g. `0.2` = 20%) |
| `timestamp`       | Signal generation time |
| `payload`         | Optional strategy-specific metadata |

This explicit structure ensures that execution remains **deterministic, testable,
and free of hidden logic**.

---

## Typical Use Cases

### 1. JoinQuant → QMT

- JoinQuant strategy generates signals (daily or intraday)
- Signals are pushed to this service via HTTP API
- QMT queries signals and executes trades accordingly

### 2. Local Research / Backtest

- Local Python scripts generate signals during research or backtesting
- Signals are written to the relay service
- Execution engine replays signals for simulation or validation

---

## API Overview

| Method | Endpoint  | Description |
|------|-----------|-------------|
| POST | `/signals` | Submit trading signals |
| GET  | `/signals` | Query pending or historical signals |
| GET  | `/health`  | Health check |

API design favors **explicitness over convenience** to avoid execution ambiguity.

---

## Environment Separation

The service supports explicit environment separation:

| Environment | Purpose |
|------------|---------|
| `dev`  | Local development |
| `test` | Automated testing (in-memory database) |
| `prod` | Production signal relay |

Environment is controlled via:

```bash
APP_ENV=dev | test | prod
```

---

## Design Principles

- Decouple signal generation from execution
- Never embed execution logic in the relay layer
- Explicit signal semantics
- Idempotent and replayable signals
- Execution engines remain stateless

---

## Project Scope

This project intentionally does **not**:

- Execute trades
- Connect to brokers
- Perform risk control
- Manage portfolios

All execution responsibilities belong to downstream engines such as **QMT**.

---

## Status

This project is under active development and serves as the foundation for a
multi-platform quantitative trading workflow.

---

## License

MIT
