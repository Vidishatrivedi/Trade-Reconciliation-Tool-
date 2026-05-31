import pandas as pd

# Load both files
sig = pd.read_csv("data/sig_ledger.csv")
cp  = pd.read_csv("data/counterparty_ledger.csv")

# === CHECK ALL 100 ROWS FOR PRICE BREAKS ===
print("=== ALL PRICE BREAKS ===")
price_breaks = sig["price"] != cp["price"]
print(sig[price_breaks][["trade_id", "counterparty", "instrument"]]
      .join(pd.DataFrame({
          "SIG price": sig["price"],
          "CP price":  cp["price"]
      }))[price_breaks])

# === CHECK ALL 100 ROWS FOR QUANTITY BREAKS ===
print("\n=== ALL QUANTITY BREAKS ===")
qty_breaks = sig["quantity"] != cp["quantity"]
print(sig[qty_breaks][["trade_id", "counterparty", "instrument"]]
      .join(pd.DataFrame({
          "SIG qty": sig["quantity"],
          "CP qty":  cp["quantity"]
      }))[qty_breaks])

# === CHECK ALL 100 ROWS FOR STATUS BREAKS ===
print("\n=== ALL STATUS BREAKS ===")
status_breaks = sig["status"] != cp["status"]
print(sig[status_breaks][["trade_id", "counterparty", "instrument"]]
      .join(pd.DataFrame({
          "SIG status": sig["status"],
          "CP status":  cp["status"]
      }))[status_breaks])

# === SUMMARY ===
print(f"\n=== SUMMARY ===")
print(f"Price breaks found:    {price_breaks.sum()}")
print(f"Quantity breaks found: {qty_breaks.sum()}")
print(f"Status breaks found:   {status_breaks.sum()}")
print(f"Total breaks found:    {price_breaks.sum() + qty_breaks.sum() + status_breaks.sum()}")