import sqlite3
import pandas as pd

# === CONNECT TO DATABASE ===
# This creates trades.db if it doesn't exist yet
conn = sqlite3.connect("trades.db")
cursor = conn.cursor()

print("Connected to database")

# === CREATE TABLES ===

# Drop tables if they already exist (so we can re-run cleanly)
cursor.execute("DROP TABLE IF EXISTS trades_sig")
cursor.execute("DROP TABLE IF EXISTS trades_cp")
cursor.execute("DROP TABLE IF EXISTS breaks")

# Create SIG trades table
cursor.execute("""
    CREATE TABLE trades_sig (
        trade_id        TEXT PRIMARY KEY,
        trade_date      TEXT,
        counterparty    TEXT,
        instrument      TEXT,
        quantity        INTEGER,
        price           REAL,
        direction       TEXT,
        settlement_date TEXT,
        status          TEXT
    )
""")

# Create counterparty trades table
cursor.execute("""
    CREATE TABLE trades_cp (
        trade_id        TEXT PRIMARY KEY,
        trade_date      TEXT,
        counterparty    TEXT,
        instrument      TEXT,
        quantity        INTEGER,
        price           REAL,
        direction       TEXT,
        settlement_date TEXT,
        status          TEXT
    )
""")

# Create breaks table
cursor.execute("""
    CREATE TABLE breaks (
        trade_id      TEXT,
        trade_date    TEXT,
        counterparty  TEXT,
        instrument    TEXT,
        break_type    TEXT,
        sig_value     TEXT,
        cp_value      TEXT,
        difference    REAL,
        severity      TEXT
    )
""")

conn.commit()
print("Tables created")

# === LOAD DATA INTO TABLES ===

# Read our CSV files
sig = pd.read_csv("data/sig_ledger.csv")
cp  = pd.read_csv("data/counterparty_ledger.csv")
breaks_df = pd.read_csv("output/breaks_report.csv")

# Load into database
sig.to_sql("trades_sig", conn, if_exists="append", index=False)
cp.to_sql("trades_cp",  conn, if_exists="append", index=False)
breaks_df.to_sql("breaks", conn, if_exists="append", index=False)

conn.commit()

print(f"Loaded {len(sig)} rows into trades_sig")
print(f"Loaded {len(cp)} rows into trades_cp")
print(f"Loaded {len(breaks_df)} rows into breaks")


# === QUERY 1 — All HIGH severity breaks ===
print("\n--- HIGH SEVERITY BREAKS ---")
query1 = """
    SELECT trade_id, counterparty, instrument, break_type, sig_value, cp_value
    FROM breaks
    WHERE severity = 'HIGH'
    ORDER BY counterparty
"""
result1 = pd.read_sql(query1, conn)
print(result1.to_string(index=False))


# === QUERY 2 — Breaks per counterparty ===
print("\n--- BREAKS PER COUNTERPARTY ---")
query2 = """
    SELECT counterparty,
           COUNT(*) as total_breaks,
           SUM(CASE WHEN severity = 'HIGH' THEN 1 ELSE 0 END) as high_breaks,
           SUM(CASE WHEN severity = 'LOW'  THEN 1 ELSE 0 END) as low_breaks
    FROM breaks
    GROUP BY counterparty
    ORDER BY total_breaks DESC
"""
result2 = pd.read_sql(query2, conn)
print(result2.to_string(index=False))


# === QUERY 3 — Unsettled trades past settlement date ===
print("\n--- OVERDUE UNSETTLED TRADES ---")
query3 = """
    SELECT trade_id, counterparty, instrument,
           trade_date, settlement_date, status
    FROM trades_sig
    WHERE status = 'PENDING'
    AND settlement_date < '2024-01-20'
    ORDER BY settlement_date
"""
result3 = pd.read_sql(query3, conn)
print(result3.to_string(index=False))
print(f"Total overdue trades: {len(result3)}")


# === QUERY 4 — Most problematic instruments ===
print("\n--- BREAKS BY INSTRUMENT ---")
query4 = """
    SELECT instrument,
           COUNT(*) as total_breaks
    FROM breaks
    GROUP BY instrument
    ORDER BY total_breaks DESC
"""
result4 = pd.read_sql(query4, conn)
print(result4.to_string(index=False))


# === CLOSE CONNECTION ===
conn.close()
print("\n Database connection closed")