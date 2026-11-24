import pandas as pd
import os

# ============================================================
# 1. FILE PATHS
# ============================================================

input_file = "../data/raw/sd254_cards.csv"
output_file = "../data/processed/clean_cards.csv"


# ============================================================
# 2. CREATE PROCESSED FOLDER
# ============================================================

os.makedirs("../data/processed", exist_ok=True)


# ============================================================
# 3. LOAD RAW DATA
# ============================================================

df = pd.read_csv(input_file)

print("Raw card records:", len(df))


# ============================================================
# 4. CREATE CARD_ID
# ============================================================

df["Card_ID"] = (
    df["User"].astype(str)
    + "_"
    + df["CARD INDEX"].astype(str)
)


# ============================================================
# 5. CLEAN CREDIT LIMIT
# ============================================================

df["Credit_Limit"] = (
    df["Credit Limit"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["Credit_Limit"] = pd.to_numeric(
    df["Credit_Limit"],
    errors="coerce"
)


# ============================================================
# 6. CONVERT ACCOUNT OPEN DATE
# ============================================================

df["Account_Open_Date"] = pd.to_datetime(
    df["Acct Open Date"],
    format="%m/%Y",
    errors="coerce"
)


# ============================================================
# 7. STANDARDIZE HAS CHIP
# ============================================================

df["Has_Chip"] = (
    df["Has Chip"]
    .astype(str)
    .str.upper()
)


# ============================================================
# 8. SELECT FINAL COLUMNS
# ============================================================

final_columns = [
    "Card_ID",
    "User",
    "CARD INDEX",
    "Card Brand",
    "Card Type",
    "Has_Chip",
    "Cards Issued",
    "Credit_Limit",
    "Account_Open_Date"
]

clean_df = df[final_columns].copy()


# ============================================================
# 9. RENAME COLUMNS
# ============================================================

clean_df = clean_df.rename(
    columns={
        "User": "User_ID",
        "CARD INDEX": "Card_Index",
        "Card Brand": "Card_Brand",
        "Card Type": "Card_Type",
        "Cards Issued": "Cards_Issued"
    }
)


# ============================================================
# 10. VALIDATION
# ============================================================

print("\n===== CLEANED CARD VALIDATION =====")

print("Rows:", len(clean_df))
print("Columns:", len(clean_df.columns))


print("\nMissing values:")
print(clean_df.isnull().sum())


print("\nDuplicate rows:")
print(clean_df.duplicated().sum())


print("\nUnique Card_ID:")
print(clean_df["Card_ID"].nunique())


print("\nUnique User_ID:")
print(clean_df["User_ID"].nunique())


print("\nCard Type distribution:")
print(clean_df["Card_Type"].value_counts())


print("\nCard Brand distribution:")
print(clean_df["Card_Brand"].value_counts())


print("\nCredit Limit summary:")
print(clean_df["Credit_Limit"].describe())


print("\nAccount Open Date range:")
print("Earliest:",
      clean_df["Account_Open_Date"].min())

print("Latest:",
      clean_df["Account_Open_Date"].max())


# ============================================================
# 11. CHECK CARD_ID DUPLICATES
# ============================================================

duplicate_card_ids = (
    clean_df["Card_ID"].duplicated().sum()
)

print("\nDuplicate Card_ID values:",
      duplicate_card_ids)


# ============================================================
# 12. DISPLAY SAMPLE
# ============================================================

print("\n===== CLEANED CARD SAMPLE =====")

print(
    clean_df.head(10)
    .to_string(index=False)
)


# ============================================================
# 13. SAVE CLEAN DATA
# ============================================================

clean_df.to_csv(
    output_file,
    index=False
)

print("\nClean card data saved to:")
print(output_file)

print("\n===== CARD CLEANING COMPLETE =====")