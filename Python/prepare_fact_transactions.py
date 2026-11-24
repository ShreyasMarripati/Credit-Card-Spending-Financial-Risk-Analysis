import pandas as pd

# ============================================================
# FILE PATHS
# ============================================================

input_file = "../data/processed/transactions_for_mysql.csv"
date_file = "../data/processed/dim_date.csv"
output_file = "../data/processed/fact_transactions.csv"

# ============================================================
# LOAD DATA
# ============================================================

transactions = pd.read_csv(input_file)
dates = pd.read_csv(date_file)

print("Transactions Loaded:", len(transactions))
print("Date Dimension Loaded:", len(dates))

# ============================================================
# CONVERT DATE
# ============================================================

transactions["Transaction_Date"] = pd.to_datetime(
    transactions["Transaction_Date"]
)

dates["Date"] = pd.to_datetime(
    dates["Date"]
)

# ============================================================
# CREATE DATE_ID DIRECTLY
# ============================================================

transactions["Date_ID"] = (
    transactions["Transaction_Date"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

# ============================================================
# VALIDATE DATE MATCH
# ============================================================

print("\n" + "=" * 60)
print("TRANSACTION → DATE VALIDATION")
print("=" * 60)

valid_date_ids = set(dates["Date_ID"])

invalid_dates = (
    ~transactions["Date_ID"].isin(valid_date_ids)
).sum()

print("Invalid Date_IDs:", invalid_dates)

print(
    "Unique Transaction Dates:",
    transactions["Date_ID"].nunique()
)

# ============================================================
# SELECT FINAL FACT COLUMNS
# ============================================================

fact_df = transactions[
    [
        "Transaction_ID",
        "User_ID",
        "Card_ID",
        "Date_ID",
        "Transaction_Time",
        "Amount",
        "Transaction_Channel",
        "Merchant_Key",
        "Error_Type",
        "Error_Flag",
        "Fraud_Flag"
    ]
].copy()

# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("FACT TRANSACTION VALIDATION")
print("=" * 60)

print("\nRows:", len(fact_df))

print(
    "Unique Transaction_IDs:",
    fact_df["Transaction_ID"].nunique()
)

print(
    "Duplicate Transaction_IDs:",
    fact_df["Transaction_ID"].duplicated().sum()
)

print(
    "Missing values:",
    fact_df.isnull().sum().sum()
)

print(
    "Fraud transactions:",
    fact_df["Fraud_Flag"].sum()
)

print(
    "Error transactions:",
    fact_df["Error_Flag"].sum()
)

print(
    "Missing Merchant Keys:",
    fact_df["Merchant_Key"].isnull().sum()
)

print(
    "Missing Date IDs:",
    fact_df["Date_ID"].isnull().sum()
)

print("\nSample:")
print(
    fact_df.head(10).to_string(index=False)
)

# ============================================================
# SAVE
# ============================================================

fact_df.to_csv(
    output_file,
    index=False
)

print("\n" + "=" * 60)
print("FACT TRANSACTION FILE CREATED")
print("=" * 60)

print("Saved to:")
print(output_file)