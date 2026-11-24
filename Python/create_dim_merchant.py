import pandas as pd
import os

# ============================================================
# FILE PATHS
# ============================================================

input_file = "../data/processed/clean_transactions.csv"
output_file = "../data/processed/dim_merchant.csv"

os.makedirs("../data/processed", exist_ok=True)

# ============================================================
# LOAD CLEAN TRANSACTIONS
# ============================================================

df = pd.read_csv(input_file)

print("Transactions Loaded:", len(df))

# ============================================================
# CREATE MERCHANT DIMENSION
# ============================================================

merchant_df = df[
    ["Merchant_ID", "Merchant_City", "Merchant_State", "MCC_Code"]
].drop_duplicates()

merchant_df = merchant_df.sort_values("Merchant_ID")

# ============================================================
# VALIDATION
# ============================================================

print("\n===== MERCHANT DIMENSION VALIDATION =====")

print("Merchant rows:", len(merchant_df))

print("\nMissing Values:")
print(merchant_df.isnull().sum())

print("\nDuplicate Merchant IDs:")
print(merchant_df["Merchant_ID"].duplicated().sum())

print("\nTop Merchant States:")
print(merchant_df["Merchant_State"].value_counts().head(10))

print("\nSample:")
print(merchant_df.head(10).to_string(index=False))

# ============================================================
# SAVE
# ============================================================

merchant_df.to_csv(output_file, index=False)

print("\nMerchant dimension saved to:")
print(output_file)

print("\n===== DIM_MERCHANT CREATED SUCCESSFULLY =====")