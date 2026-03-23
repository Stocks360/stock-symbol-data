import pandas as pd

# STEP 1: Load existing file
try:
    existing = pd.read_csv("bse_nse_map.csv", header=None)
    existing.columns = ["bse", "nse"]
except:
    existing = pd.DataFrame(columns=["bse", "nse"])

existing_nse = set(existing["nse"].astype(str))

# STEP 2: Load NSE list
nse_url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
nse = pd.read_csv(nse_url)

# STEP 3: Add only missing symbols
new_rows = []

for symbol in nse["SYMBOL"]:
    symbol = str(symbol).strip()

    if symbol not in existing_nse:
        new_rows.append([symbol, symbol])

new_df = pd.DataFrame(new_rows, columns=["bse", "nse"])

# STEP 4: Merge safely
final = pd.concat([existing, new_df], ignore_index=True)

final = final.drop_duplicates(subset="bse")

# STEP 5: Save EXACT format (no header)
final.to_csv("bse_nse_map.csv", index=False, header=False)

print(f"Total symbols: {len(final)}")
