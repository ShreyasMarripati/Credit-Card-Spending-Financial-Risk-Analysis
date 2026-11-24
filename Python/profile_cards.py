import pandas as pd

# ============================================================
# 1. LOAD DATA
# ============================================================

file_path = "../data/raw/sd254_cards.csv"

df = pd.read_csv(file_path)


# ============================================================
# 2. BASIC INFORMATION
# ============================================================

print("===== BASIC INFORMATION =====")

print("Rows:", len(df))
print("Columns:", len(df.columns))


# ============================================================
# 3. UNIQUE VALUES
# ============================================================

print("\n===== UNIQUE VALUES =====")

print("Unique Users:", df["User"].nunique())
print("Unique Card Index:", df["CARD INDEX"].nunique())
print("Unique Card Brands:", df["Card Brand"].nunique())
print("Unique Card Types:", df["Card Type"].nunique())


# ============================================================
# 4. CARD BRAND DISTRIBUTION
# ============================================================

print("\n===== CARD BRAND DISTRIBUTION =====")

print(df["Card Brand"].value_counts())


# ============================================================
# 5. CARD TYPE DISTRIBUTION
# ============================================================

print("\n===== CARD TYPE DISTRIBUTION =====")

print(df["Card Type"].value_counts())


# ============================================================
# 6. CARDS PER USER
# ============================================================

print("\n===== CARDS PER USER =====")

cards_per_user = df.groupby("User").size()

print(cards_per_user.describe())


# ============================================================
# 7. CHECK USER + CARD INDEX UNIQUENESS
# ============================================================

print("\n===== USER + CARD INDEX UNIQUENESS =====")

duplicate_card_keys = df.duplicated(
    subset=["User", "CARD INDEX"]
).sum()

print("Duplicate User + Card Index combinations:",
      duplicate_card_keys)


# ============================================================
# 8. CREDIT LIMIT BY CARD TYPE
# ============================================================

print("\n===== CREDIT LIMIT BY CARD TYPE =====")

# Remove $ and commas, then convert to number
df["Credit_Limit_Numeric"] = (
    df["Credit Limit"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)

credit_limit_by_type = df.groupby("Card Type")["Credit_Limit_Numeric"].agg(
    ["count", "min", "max", "mean"]
)

print(credit_limit_by_type)


# ============================================================
# 9. ZERO CREDIT LIMIT BY CARD TYPE
# ============================================================

print("\n===== ZERO CREDIT LIMIT BY CARD TYPE =====")

zero_limit = (
    df["Credit_Limit_Numeric"] == 0
)

print(
    df.loc[zero_limit, "Card Type"]
    .value_counts()
)


# ============================================================
# 10. HAS CHIP DISTRIBUTION
# ============================================================

print("\n===== HAS CHIP DISTRIBUTION =====")

print(df["Has Chip"].value_counts())


# ============================================================
# 11. CARDS ISSUED DISTRIBUTION
# ============================================================

print("\n===== CARDS ISSUED SUMMARY =====")

print(df["Cards Issued"].describe())


# ============================================================
# 12. ACCOUNT OPEN DATE SAMPLE
# ============================================================

print("\n===== ACCOUNT OPEN DATE SAMPLE =====")

print(df["Acct Open Date"].head(10).to_string(index=False))


# ============================================================
# 13. MISSING VALUES
# ============================================================

print("\n===== MISSING VALUES =====")

print(df.isnull().sum())


# ============================================================
# 14. DUPLICATE ROWS
# ============================================================

print("\n===== DUPLICATE ROWS =====")

print(df.duplicated().sum())


# ============================================================
# 15. FIRST 5 ROWS
# ============================================================

print("\n===== FIRST 5 ROWS =====")

print(df.head())


# ============================================================
# COMPLETE
# ============================================================

print("\n===== CARD PROFILING COMPLETE =====")