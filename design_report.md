# Trading Backtester — Assignment 6 Final Design Report

**Student:** x3622555  
**Repository:** [https://github.com/x3622555-ship-it/trading-architecture-assignment6](https://github.com/x3622555-ship-it/trading-architecture-assignment6)  
**Phase:** F (Final Verification and Reporting)

---

## 1. Project Overview

This project implements a modular **trading backtesting framework** using multiple software design patterns.  
It simulates financial data, applies trading strategies, executes trades through a command system, and computes performance metrics such as total return and Sharpe ratio.

---

## 2. Implemented Design Patterns

| Pattern | Module | Description |
|----------|---------|-------------|
| **Factory** | `patterns/factory.py` | Dynamically creates instruments (Stock, Bond, ETF). |
| **Singleton** | `patterns/singleton.py` | Ensures only one global configuration instance. |
| **Builder** | `patterns/builder.py` | Builds `Portfolio` objects with positions. |
| **Decorator** | `patterns/decorator.py` | Adds risk metrics (volatility, max drawdown). |
| **Adapter** | `patterns/adapter.py` | Normalizes different data formats for the engine. |
| **Composite** | `patterns/composite.py` | Combines multiple portfolios into a unified view. |
| **Strategy** | `patterns/strategy.py` | Contains trading algorithms (e.g., Moving Average Crossover). |
| **Observer** | `patterns/observer.py` | Publishes market events to logging and alert observers. |
| **Command** | `patterns/command.py` | Encapsulates trading operations (execute, undo). |
| **Engine** | `engine.py` | Coordinates tick data, strategies, and executions. |
| **Reporting** | `reporting.py` | Calculates equity curves, total returns, and Sharpe ratios. |

---

## 3. Testing and Verification

Automated tests were written using **pytest** and are located in the `tests/` folder.

To run tests:
```bash
venv\Scripts\activate
python -m pytest -q
