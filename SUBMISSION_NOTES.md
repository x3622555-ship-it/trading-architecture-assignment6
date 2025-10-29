Assignment 6 — Trading Backtester
Student: x3622555
Repo: https://github.com/x3622555-ship-it/trading-architecture-assignment6

How to run:
1. Clone repo: git clone <repo-url>
2. cd trading_backtester
3. python -m venv venv
4. venv\Scripts\activate
5. python -m pip install -r requirements.txt
6. python data/data_generator.py   # if market_data.csv not present
7. python -m pytest -q
8. python -m scripts.demo_final

Files included:
- src/: all source code
- tests/: pytest unit tests
- scripts/demo_final.py: demonstration script
- design_report.md: design writeup

Notes:
- All tests passed locally on Windows with Python 3.14
- If demo fails due to missing market_data.csv, run data/data_generator.py
