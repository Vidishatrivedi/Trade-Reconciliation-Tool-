# Trade Reconciliation & Break Detection Tool

## Overview
An automated trade reconciliation system built in Python that simulates
real-world operations workflows at trading firms. The tool ingests two
trade ledgers, detects position breaks and settlement mismatches, stores
results in a SQL database, and generates formatted Excel reports.

---

## What Problem Does This Solve?
Trading firms process thousands of trades daily across multiple
counterparties. Each trade is recorded independently by both sides —
SIG's internal system and the counterparty's system. These records
must match exactly. When they don't, it's called a **break**.

Finding breaks manually across thousands of trades takes hours.
This tool does it in seconds.

---

## Features
- Simulates two realistic trade ledgers (100 trades each)
- Detects three types of breaks:
  - Price breaks — same trade, different price recorded
  - Quantity breaks — same trade, different share count
  - Status breaks — one side settled, other side pending
- Assigns severity levels (HIGH / LOW) to each break
- Stores all trade data in a SQLite database
- SQL queries identify overdue unsettled trades and worst counterparties
- Generates a formatted multi-sheet Excel report with colour coding

---

## Tech Stack
| Tool       | Purpose                          |
|------------|----------------------------------|
| Python     | Core language                    |
| pandas     | Data manipulation and comparison |
| SQLite     | Trade data storage and querying  |
| openpyxl   | Excel report generation          |

---

## How to Run

### 1. Install dependencies
pip install pandas openpyxl faker

### 2. Run the full pipeline
python main.py

### 3. View the report
Open output/reconciliation_report.xlsx

---

## Project Structure

---

## Sample Output

### Break Detection Summary
| Break Type | Count |
|------------|-------|
| Price      | 10    |
| Quantity   | 8     |
| Status     | 6     |
| **Total**  | **24**|

### Counterparty Risk Ranking
Counterparties are automatically ranked by number of breaks
and assigned HIGH / MEDIUM / LOW risk levels.

---

## Real World Relevance
This tool mirrors workflows used by operations teams at
trading firms including:
- Morning reconciliation before market open
- Settlement failure detection (T+2 monitoring)
- Counterparty risk ranking
- Break report distribution to management

---

## Author
Vidisha Trivedi
trivedividisha@gmail.com