import pandas as pd
import os

# ============================================================
# FILE PATHS
# ============================================================

input_file = "../data/processed/clean_transactions.csv"

merchant_output = "../data/processed/dim_merchant.csv"
transaction_output = "../data/processed/transactions_for_mysql.csv"

# ============================================================
# LOAD CLEAN TRANSACTIONS
# ============================================================

df = pd.read_csv(input_file)

print("Transactions Loaded:", len(df))

# ============================================================
# CREATE UNIQUE MERCHANT DIMENSION
# ============================================================

merchant_columns = [
    "Merchant_ID",
    "Merchant_City",
    "Merchant_State",
    "MCC_Code"
]

merchant_df = (
    df[merchant_columns]
    .drop_duplicates()
    .reset_index(drop=True)
)

# ============================================================
# CREATE SURROGATE MERCHANT KEY
# ============================================================

merchant_df.insert(
    0,
    "Merchant_Key",
    range(1, len(merchant_df) + 1)
)

# ============================================================
# VALIDATE MERCHANT DIMENSION
# ============================================================

print("\n" + "=" * 60)
print("MERCHANT DIMENSION VALIDATION")
print("=" * 60)

print("\nMerchant rows:", len(merchant_df))

print("\nMissing Values:")
print(merchant_df.isnull().sum())

print("\nDuplicate Merchant Keys:")
print(merchant_df["Merchant_Key"].duplicated().sum())

print("\nDuplicate Merchant IDs:")
print(merchant_df["Merchant_ID"].duplicated().sum())

print("\nUnique Merchant Keys:")
print(merchant_df["Merchant_Key"].nunique())

print("\nUnique Source Merchant IDs:")
print(merchant_df["Merchant_ID"].nunique())

print("\nSample:")
print(
    merchant_df.head(10).to_string(index=False)
)

# ============================================================
# ADD MERCHANT KEY TO TRANSACTIONS
# ============================================================

df_final = df.merge(
    merchant_df,
    on=[
        "Merchant_ID",
        "Merchant_City",
        "Merchant_State",
        "MCC_Code"
    ],
    how="left",
    validate="many_to_one"
)

# ============================================================
# VALIDATE TRANSACTION MERCHANT MATCH
# ============================================================

print("\n" + "=" * 60)
print("TRANSACTION → MERCHANT KEY VALIDATION")
print("=" * 60)

print(
    "\nTransactions:",
    len(df_final)
)

print(
    "Transactions with missing Merchant_Key:",
    df_final["Merchant_Key"].isnull().sum()
)

print(
    "Unique Merchant Keys used by transactions:",
    df_final["Merchant_Key"].nunique()
)

# ============================================================
# SELECT FINAL TRANSACTION COLUMNS
# ============================================================

transaction_columns = [
    "Transaction_ID",
    "User_ID",
    "Card_ID",
    "Transaction_Date",
    "Transaction_Time",
    "Amount",
    "Transaction_Channel",
    "Merchant_Key",
    "Error_Type",
    "Error_Flag",
    "Fraud_Flag"
]

transaction_final = df_final[transaction_columns].copy()

# ============================================================
# FINAL TRANSACTION VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("FINAL TRANSACTION VALIDATION")
print("=" * 60)

print(
    "\nRows:",
    len(transaction_final)
)

print(
    "Columns:",
    len(transaction_final.columns)
)

print(
    "Unique Transaction_IDs:",
    transaction_final["Transaction_ID"].nunique()
)

print(
    "Missing Merchant Keys:",
    transaction_final["Merchant_Key"].isnull().sum()
)

print(
    "Fraud transactions:",
    transaction_final["Fraud_Flag"].sum()
)

print("\nSample:")
print(
    transaction_final.head(10).to_string(index=False)
)

# ============================================================
# SAVE FILES
# ============================================================

merchant_df.to_csv(
    merchant_output,
    index=False
)

transaction_final.to_csv(
    transaction_output,
    index=False
)

print("\n" + "=" * 60)
print("FILES CREATED")
print("=" * 60)

print("\nMerchant dimension:")
print(merchant_output)

print("\nTransaction file for MySQL:")
print(transaction_output)

print("\n===== MERCHANT ETL COMPLETE =====")