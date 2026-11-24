import pandas as pd
import os


# ============================================================
# 1. FILE PATHS
# ============================================================

input_file = "../data/raw/credit_card_transactions_project.csv"
output_file = "../data/processed/clean_transactions.csv"


# ============================================================
# 2. CREATE PROCESSED FOLDER
# ============================================================

os.makedirs("../data/processed", exist_ok=True)


# ============================================================
# 3. LOAD RAW TRANSACTION DATA
# ============================================================

df = pd.read_csv(input_file)

print("Raw transaction records:", len(df))


# ============================================================
# 4. CREATE TRANSACTION_ID
# ============================================================

# Create a unique ID for every transaction.
#
# The source dataset does not provide a suitable transaction
# primary key, so we generate one based on the row position.

df["Transaction_ID"] = range(1, len(df) + 1)


# ============================================================
# 5. CREATE CARD_ID
# ============================================================

# Card is only unique within a User.
#
# Example:
# User = 1404
# Card = 1
#
# Card_ID = 1404_1

df["Card_ID"] = (
    df["User"].astype(str)
    + "_"
    + df["Card"].astype(str)
)


# ============================================================
# 6. CLEAN TRANSACTION AMOUNT
# ============================================================

df["Amount"] = (
    df["Amount"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["Amount"] = pd.to_numeric(
    df["Amount"],
    errors="coerce"
)


# ============================================================
# 7. CREATE TRANSACTION DATE
# ============================================================

df["Transaction_Date"] = pd.to_datetime(
    dict(
        year=df["Year"],
        month=df["Month"],
        day=df["Day"]
    ),
    errors="coerce"
)


# ============================================================
# 8. STANDARDIZE TRANSACTION CHANNEL
# ============================================================

df["Transaction_Channel"] = (
    df["Use Chip"]
    .astype(str)
    .str.strip()
)


# ============================================================
# 9. CREATE FRAUD FLAG
# ============================================================

df["Fraud_Flag"] = (
    df["Is Fraud?"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map({
        "yes": 1,
        "no": 0
    })
)


# ============================================================
# 10. CLEAN ERROR INFORMATION
# ============================================================

# Blank Errors? means no error was recorded.
#
# We convert:
# missing → "No Error"

df["Error_Type"] = (
    df["Errors?"]
    .fillna("No Error")
    .astype(str)
    .str.strip()
)

# Create an easy numerical error flag

df["Error_Flag"] = (
    df["Error_Type"] != "No Error"
).astype(int)


# ============================================================
# 11. HANDLE MISSING MERCHANT STATE
# ============================================================

df["Merchant_State"] = (
    df["Merchant State"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)


# ============================================================
# 12. CLEAN MERCHANT CITY
# ============================================================

df["Merchant_City"] = (
    df["Merchant City"]
    .astype(str)
    .str.strip()
)


# ============================================================
# 13. CREATE FINAL FACT TABLE COLUMNS
# ============================================================

final_columns = [
    "Transaction_ID",
    "User",
    "Card_ID",
    "Transaction_Date",
    "Time",
    "Amount",
    "Transaction_Channel",
    "Merchant Name",
    "Merchant_City",
    "Merchant_State",
    "MCC",
    "Error_Type",
    "Error_Flag",
    "Fraud_Flag"
]

clean_df = df[final_columns].copy()


# ============================================================
# 14. RENAME COLUMNS
# ============================================================

clean_df = clean_df.rename(
    columns={
        "User": "User_ID",
        "Time": "Transaction_Time",
        "Merchant Name": "Merchant_ID",
        "MCC": "MCC_Code"
    }
)


# ============================================================
# 15. VALIDATION — ROW COUNT
# ============================================================

print("\n===== CLEANED TRANSACTION VALIDATION =====")

print("Rows:", len(clean_df))
print("Columns:", len(clean_df.columns))


# ============================================================
# 16. VALIDATION — MISSING VALUES
# ============================================================

print("\nMissing values:")

print(clean_df.isnull().sum())


# ============================================================
# 17. VALIDATION — DUPLICATES
# ============================================================

print("\nDuplicate rows:")

print(clean_df.duplicated().sum())


# ============================================================
# 18. VALIDATION — TRANSACTION ID
# ============================================================

print("\nUnique Transaction_ID:")

print(clean_df["Transaction_ID"].nunique())

print("\nDuplicate Transaction_ID:")

print(
    clean_df["Transaction_ID"].duplicated().sum()
)


# ============================================================
# 19. VALIDATION — CARD ID
# ============================================================

print("\nUnique Card_ID:")

print(clean_df["Card_ID"].nunique())


# ============================================================
# 20. TRANSACTION AMOUNT SUMMARY
# ============================================================

print("\n===== AMOUNT SUMMARY =====")

print(
    clean_df["Amount"].describe()
)


# ============================================================
# 21. NEGATIVE / ZERO / POSITIVE TRANSACTIONS
# ============================================================

print("\n===== TRANSACTION AMOUNT TYPES =====")

negative_count = (
    clean_df["Amount"] < 0
).sum()

zero_count = (
    clean_df["Amount"] == 0
).sum()

positive_count = (
    clean_df["Amount"] > 0
).sum()

print("Negative transactions:", negative_count)
print("Zero transactions:", zero_count)
print("Positive transactions:", positive_count)


# ============================================================
# 22. FRAUD SUMMARY
# ============================================================

print("\n===== FRAUD SUMMARY =====")

print(
    clean_df["Fraud_Flag"]
    .value_counts()
    .sort_index()
)

print(
    "Total fraud transactions:",
    clean_df["Fraud_Flag"].sum()
)


# ============================================================
# 23. ERROR SUMMARY
# ============================================================

print("\n===== ERROR SUMMARY =====")

print(
    clean_df["Error_Flag"]
    .value_counts()
    .sort_index()
)

print(
    "Total transactions with errors:",
    clean_df["Error_Flag"].sum()
)


# ============================================================
# 24. TRANSACTION CHANNEL
# ============================================================

print("\n===== TRANSACTION CHANNEL =====")

print(
    clean_df["Transaction_Channel"]
    .value_counts()
)


# ============================================================
# 25. DATE VALIDATION
# ============================================================

print("\n===== DATE VALIDATION =====")

print(
    "Earliest transaction:",
    clean_df["Transaction_Date"].min()
)

print(
    "Latest transaction:",
    clean_df["Transaction_Date"].max()
)

print(
    "Invalid dates:",
    clean_df["Transaction_Date"].isna().sum()
)


# ============================================================
# 26. MERCHANT STATE
# ============================================================

print("\n===== MERCHANT STATE =====")

print(
    clean_df["Merchant_State"]
    .value_counts()
    .head(15)
)


# ============================================================
# 27. SAMPLE
# ============================================================

print("\n===== CLEANED TRANSACTION SAMPLE =====")

print(
    clean_df.head(10)
    .to_string(index=False)
)


# ============================================================
# 28. SAVE CLEAN DATA
# ============================================================

clean_df.to_csv(
    output_file,
    index=False
)

print("\nClean transaction data saved to:")

print(output_file)


# ============================================================
# COMPLETE
# ============================================================

print("\n===== TRANSACTION CLEANING COMPLETE =====")