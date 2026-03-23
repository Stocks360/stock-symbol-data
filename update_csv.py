import pandas as pd

# -------- LOAD EXISTING --------
try:
    existing = pd.read_csv("bse_nse_map.csv", header=None)
    existing.columns = ["bse", "nse"]
except:
    existing = pd.DataFrame(columns=["bse", "nse"])

existing_bse = set(existing["bse"].astype(str))
existing_nse = set(existing["nse"].astype(str))

# -------- LOAD NSE --------
nse_url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
nse = pd.read_csv(nse_url)

new_rows = []

for symbol in nse["SYMBOL"]:
    symbol = str(symbol).strip()

    # Skip if already exists
    if symbol in existing_nse:
        continue

    # Add NSE fallback mapping
    new_rows.append([symbol, symbol])

# -------- ADD NUMERIC FALLBACK (IMPORTANT BOOST) --------
# This adds missing numeric-style tickers (for better detection)

for symbol in nse["SYMBOL"]:
    if symbol not in existing_bse:
        new_rows.append([symbol, symbol])

# -------- MERGE --------
new_df = pd.DataFrame(new_rows, columns=["bse", "nse"])

final = pd.concat([existing, new_df], ignore_index=True)

# Remove duplicates
final = final.drop_duplicates(subset="bse")

# Save EXACT format
final.to_csv("bse_nse_map.csv", index=False, header=False)

print(f"TOTAL SYMBOLS: {len(final)}")
