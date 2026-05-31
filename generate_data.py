import pandas as pd 
import random 
from datetime import date, timedelta 

# === REFERENCE DATA ===
counterparties = [
    "Goldman Sachs",
    "JP Morgan",
    "Morgan Stanley",
    "Citadel",
    "Jane Street"
]

instruments = [
    "AAPL", "GOOGL", "MSFT",
    "AMZN", "NVDA", "TSLA",
    "SPY", "QQQ"
]

statuses = ["SETTLED", "PENDING", "FAILED"]

# === GENERATE ONE TRADE ===
def generate_trade(trade_id, trade_date):
    return {
        "trade_id":         f"TRD-{trade_id:04d}",
        "trade_date":       trade_date.strftime("%Y-%m-%d"),
        "counterparty":     random.choice(counterparties),
        "instrument":       random.choice(instruments),
        "quantity":         random.randint(100, 10000),
        "price":            round(random.uniform(10.0, 500.0), 2),
        "direction":        random.choice(["BUY", "SELL"]),
        "settlement_date":  (trade_date + timedelta(days=2)).strftime("%Y-%m-%d"),
        "status":           random.choice(statuses)
    }

    # === GENERATE 100 TRADES ===
random.seed(42)
start_date = date(2024, 1, 15)
trades = []

for i in range(1, 101):
    trade_date = start_date + timedelta(days=random.randint(0, 9))
    trades.append(generate_trade(i, trade_date))

# === CREATE SIG'S LEDGER ===
sig_df = pd.DataFrame(trades)

# === CREATE COUNTERPARTY LEDGER WITH BREAKS ===
cp_df = sig_df.copy()

# Break type 1 - Price breaks (10 trades)
price_break_ids = random.sample(range(100), 10)
for i in price_break_ids:
    cp_df.at[i, "price"] = round(cp_df.at[i, "price"] + random.uniform(0.5, 5.0), 2)

# Break type 2 - Quantity breaks (8 trades)
qty_break_ids = random.sample(range(100), 8)
for i in qty_break_ids:
    cp_df.at[i, "quantity"] = cp_df.at[i, "quantity"] + random.randint(10, 200)

# Break type 3 - Status breaks (6 trades)
status_break_ids = random.sample(range(100), 6)
for i in status_break_ids:
    current = cp_df.at[i, "status"]
    other_statuses = [s for s in statuses if s != current]
    cp_df.at[i, "status"] = random.choice(other_statuses)

# === SAVE BOTH TO CSV ===
sig_df.to_csv("data/sig_ledger.csv", index=False)
cp_df.to_csv("data/counterparty_ledger.csv", index=False)

print(f"Generated 100 trades")
print(f"Price breaks inserted:    {len(price_break_ids)}")
print(f"Quantity breaks inserted: {len(qty_break_ids)}")
print(f"Status breaks inserted:   {len(status_break_ids)}")
print(f"Files saved to /data folder")