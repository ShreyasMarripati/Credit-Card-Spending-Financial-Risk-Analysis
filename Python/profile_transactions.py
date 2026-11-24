import pandas as pd

# ============================================================
# 1. LOAD TRANSACTION DATA
# ============================================================

file_path = "../data/raw/credit_card_transactions_project.csv"

df = pd.read_csv(file_path)


# ============================================================
# 2. BASIC INFORMATION
# ============================================================

print("===== BASIC INFORMATION =====")

print("Rows:", len(df))
print("Columns:", len(df.columns))


# ============================================================
# 3. COLUMN NAMES
# ============================================================

print("\n===== COLUMN NAMES =====")

print(df.columns.tolist())


# ============================================================
# 4. DATA TYPES
# ============================================================

print("\n===== DATA TYPES =====")

print(df.dtypes)


# ============================================================
# 5. UNIQUE VALUES
# ============================================================

print("\n===== UNIQUE VALUES =====")

print("Unique Users:", df["User"].nunique())
print("Unique Card Index:", df["Card"].nunique())
print("Unique Merchants:", df["Merchant Name"].nunique())
print("Unique MCC Categories:", df["MCC"].nunique())
print("Unique Merchant Cities:", df["Merchant City"].nunique())
print("Unique Merchant States:", df["Merchant State"].nunique())


# ============================================================
# 6. MISSING VALUES
# ============================================================

print("\n===== MISSING VALUES =====")

print(df.isnull().sum())


# ============================================================
# 7. DUPLICATE ROWS
# ============================================================

print("\n===== DUPLICATE ROWS =====")

print(df.duplicated().sum())


# ============================================================
# 8. TRANSACTION AMOUNT SAMPLE
# ============================================================

print("\n===== TRANSACTION AMOUNT SAMPLE =====")

print(
    df["Amount"]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 9. TRANSACTION CHANNEL DISTRIBUTION
# ============================================================

print("\n===== TRANSACTION CHANNEL DISTRIBUTION =====")

print(df["Use Chip"].value_counts())


# ============================================================
# 10. FRAUD DISTRIBUTION
# ============================================================

print("\n===== FRAUD DISTRIBUTION =====")

print(df["Is Fraud?"].value_counts())


# ============================================================
# 11. ERROR DISTRIBUTION
# ============================================================

print("\n===== ERROR DISTRIBUTION =====")

print(df["Errors?"].value_counts(dropna=False))


# ============================================================
# 12. YEAR DISTRIBUTION
# ============================================================

print("\n===== YEAR DISTRIBUTION =====")

print(df["Year"].value_counts().sort_index())


# ============================================================
# 13. MONTH DISTRIBUTION
# ============================================================

print("\n===== MONTH DISTRIBUTION =====")

print(df["Month"].value_counts().sort_index())


# ============================================================
# 14. MCC DISTRIBUTION
# ============================================================

print("\n===== TOP MCC CATEGORIES =====")

print(df["MCC"].value_counts().head(20))


# ============================================================
# 15. MERCHANT DISTRIBUTION
# ============================================================

print("\n===== TOP MERCHANTS =====")

print(df["Merchant Name"].value_counts().head(20))


# ============================================================
# 16. TRANSACTION AMOUNT CLEANING
# ============================================================

# Convert "$1,234.56" into numeric 1234.56
amount_numeric = (
    df["Amount"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["Amount_Numeric"] = pd.to_numeric(
    amount_numeric,
    errors="coerce"
)


# ============================================================
# 17. TRANSACTION AMOUNT SUMMARY
# ============================================================

print("\n===== TRANSACTION AMOUNT SUMMARY =====")

print(df["Amount_Numeric"].describe())


# ============================================================
# 18. NEGATIVE TRANSACTIONS
# ============================================================

print("\n===== NEGATIVE TRANSACTIONS =====")

negative_count = (
    df["Amount_Numeric"] < 0
).sum()

print("Negative transactions:", negative_count)


# ============================================================
# 19. ZERO TRANSACTIONS
# ============================================================

print("\n===== ZERO TRANSACTIONS =====")

zero_count = (
    df["Amount_Numeric"] == 0
).sum()

print("Zero-value transactions:", zero_count)


# ============================================================
# 20. POSITIVE TRANSACTIONS
# ============================================================

print("\n===== POSITIVE TRANSACTIONS =====")

positive_count = (
    df["Amount_Numeric"] > 0
).sum()

print("Positive transactions:", positive_count)


# ============================================================
# 21. DATE RANGE
# ============================================================

print("\n===== DATE RANGE =====")

df["Transaction_Date"] = pd.to_datetime(
    dict(
        year=df["Year"],
        month=df["Month"],
        day=df["Day"]
    ),
    errors="coerce"
)

print("Earliest transaction:",
      df["Transaction_Date"].min())

print("Latest transaction:",
      df["Transaction_Date"].max())

print("Invalid dates:",
      df["Transaction_Date"].isna().sum())


# ============================================================
# 22. TRANSACTIONS PER USER
# ============================================================

print("\n===== TRANSACTIONS PER USER =====")

transactions_per_user = df.groupby("User").size()

print(transactions_per_user.describe())


# ============================================================
# 23. TRANSACTIONS PER CARD INDEX
# ============================================================

print("\n===== TRANSACTIONS PER CARD INDEX =====")

transactions_per_card = df.groupby("Card").size()

print(transactions_per_card.describe())


# ============================================================
# 24. TOP SPENDING USERS
# ============================================================

print("\n===== TOP SPENDING USERS =====")

top_users = (
    df.groupby("User")["Amount_Numeric"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_users)


# ============================================================
# 25. TOP SPENDING STATES
# ============================================================

print("\n===== TOP SPENDING STATES =====")

top_states = (
    df.groupby("Merchant State")["Amount_Numeric"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_states)


# ============================================================
# 26. COMPLETE
# ============================================================

print("\n===== TRANSACTION PROFILING COMPLETE =====")