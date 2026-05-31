import pandas as pd
from datetime import date

# === LOAD BOTH LEDGERS ===
print("Loading ledgers...")

sig = pd.read_csv("data/sig_ledger.csv")
cp  = pd.read_csv("data/counterparty_ledger.csv")

print(f"SIG ledger:          {len(sig)} trades loaded")
print(f"Counterparty ledger: {len(cp)} trades loaded")

# === MERGE BOTH LEDGERS SIDE BY SIDE ===
merged = pd.merge(
    sig, cp,
    on="trade_id",
    suffixes=("_sig", "_cp")
)

print(f"Merged table:        {len(merged)} trades matched")

# === DETECT BREAKS ===
breaks = []

for _, row in merged.iterrows():

    # --- Price break ---
    if row["price_sig"] != row["price_cp"]:
        breaks.append({
            "trade_id":       row["trade_id"],
            "trade_date":     row["trade_date_sig"],
            "counterparty":   row["counterparty_sig"],
            "instrument":     row["instrument_sig"],
            "break_type":     "PRICE",
            "sig_value":      row["price_sig"],
            "cp_value":       row["price_cp"],
            "difference":     round(row["price_cp"] - row["price_sig"], 2),
            "severity":       "HIGH" if abs(row["price_cp"] - row["price_sig"]) > 2 else "LOW"
        })

    # --- Quantity break ---
    if row["quantity_sig"] != row["quantity_cp"]:
        breaks.append({
            "trade_id":       row["trade_id"],
            "trade_date":     row["trade_date_sig"],
            "counterparty":   row["counterparty_sig"],
            "instrument":     row["instrument_sig"],
            "break_type":     "QUANTITY",
            "sig_value":      row["quantity_sig"],
            "cp_value":       row["quantity_cp"],
            "difference":     row["quantity_cp"] - row["quantity_sig"],
            "severity":       "HIGH" if abs(row["quantity_cp"] - row["quantity_sig"]) > 100 else "LOW"
        })

    # --- Status break ---
    if row["status_sig"] != row["status_cp"]:
        breaks.append({
            "trade_id":       row["trade_id"],
            "trade_date":     row["trade_date_sig"],
            "counterparty":   row["counterparty_sig"],
            "instrument":     row["instrument_sig"],
            "break_type":     "STATUS",
            "sig_value":      row["status_sig"],
            "cp_value":       row["status_cp"],
            "difference":     None,
            "severity":       "HIGH" if "FAILED" in [row["status_sig"], row["status_cp"]] else "LOW"
        })

# Convert breaks list into a DataFrame
breaks_df = pd.DataFrame(breaks)

print(f"\n=== BREAKS DETECTED ===")
print(f"Total breaks:    {len(breaks_df)}")
print(f"Price breaks:    {len(breaks_df[breaks_df['break_type'] == 'PRICE'])}")
print(f"Quantity breaks: {len(breaks_df[breaks_df['break_type'] == 'QUANTITY'])}")
print(f"Status breaks:   {len(breaks_df[breaks_df['break_type'] == 'STATUS'])}")
print(f"HIGH severity:   {len(breaks_df[breaks_df['severity'] == 'HIGH'])}")
print(f"LOW severity:    {len(breaks_df[breaks_df['severity'] == 'LOW'])}")

# === COUNTERPARTY SUMMARY ===
cp_summary = (
    breaks_df.groupby("counterparty")["break_type"]
    .count()
    .reset_index()
    .rename(columns={"break_type": "total_breaks"})
    .sort_values("total_breaks", ascending=False)
)

print(f"\n=== BREAKS BY COUNTERPARTY ===")
print(cp_summary.to_string(index=False))

# === SAVE RESULTS ===
breaks_df.to_csv("output/breaks_report.csv", index=False)
cp_summary.to_csv("output/counterparty_summary.csv", index=False)

print(f"\n breaks_report.csv saved to /output")
print(f" counterparty_summary.csv saved to /output")