import pandas as pd

# ============================================================
# 1. LOAD THE CUSTOMER DATASET
# ============================================================

file_path = "../data/raw/sd254_users.csv"

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

print("Unique Person names:", df["Person"].nunique())
print("Unique States:", df["State"].nunique())
print("Unique Genders:", df["Gender"].nunique())


# ============================================================
# 6. GENDER DISTRIBUTION
# ============================================================

print("\n===== GENDER DISTRIBUTION =====")

print(df["Gender"].value_counts())


# ============================================================
# 7. STATE DISTRIBUTION
# ============================================================

print("\n===== STATE DISTRIBUTION =====")

print(df["State"].value_counts().head(15))


# ============================================================
# 8. AGE SUMMARY
# ============================================================

print("\n===== AGE SUMMARY =====")

print(df["Current Age"].describe())


# ============================================================
# 9. FICO SCORE SUMMARY
# ============================================================

print("\n===== FICO SUMMARY =====")

print(df["FICO Score"].describe())


# ============================================================
# 10. NUMBER OF CREDIT CARDS SUMMARY
# ============================================================

print("\n===== CREDIT CARD COUNT SUMMARY =====")

print(df["Num Credit Cards"].describe())


# ============================================================
# 11. INCOME SAMPLE
# ============================================================

print("\n===== INCOME SAMPLE =====")

# Find the actual income column automatically
income_columns = [
    col for col in df.columns
    if "Yearly Income" in col
]

if len(income_columns) > 0:

    income_col = income_columns[0]

    print("Actual income column:", repr(income_col))

    print(
        df[income_col]
        .head(10)
        .to_string(index=False)
    )

else:

    print("Yearly Income column was not found.")


# ============================================================
# 12. DEBT SAMPLE
# ============================================================

print("\n===== DEBT SAMPLE =====")

# Find the actual debt column automatically
debt_columns = [
    col for col in df.columns
    if "Total Debt" in col
]

if len(debt_columns) > 0:

    debt_col = debt_columns[0]

    print("Actual debt column:", repr(debt_col))

    print(
        df[debt_col]
        .head(10)
        .to_string(index=False)
    )

else:

    print("Total Debt column was not found.")


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
# END
# ============================================================

print("\n===== PROFILING COMPLETE =====")