import pandas as pd
import os

# ============================================================
# 1. FILE PATHS
# ============================================================

input_file = "../data/raw/sd254_users.csv"
output_file = "../data/processed/clean_customers.csv"


# ============================================================
# 2. CREATE PROCESSED FOLDER IF IT DOES NOT EXIST
# ============================================================

os.makedirs("../data/processed", exist_ok=True)


# ============================================================
# 3. LOAD RAW DATA
# ============================================================

df = pd.read_csv(input_file)

print("Raw customer records:", len(df))


# ============================================================
# 4. CREATE USER_ID
# ============================================================

# The row index corresponds to the User value
# used in the cards and transaction datasets.

df["User_ID"] = df.index


# ============================================================
# 5. CLEAN YEARLY INCOME
# ============================================================

df["Yearly_Income"] = (
    df["Yearly Income - Person"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["Yearly_Income"] = pd.to_numeric(
    df["Yearly_Income"],
    errors="coerce"
)


# ============================================================
# 6. CLEAN TOTAL DEBT
# ============================================================

df["Total_Debt"] = (
    df["Total Debt"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["Total_Debt"] = pd.to_numeric(
    df["Total_Debt"],
    errors="coerce"
)


# ============================================================
# 7. CREATE AGE GROUP
# ============================================================

def assign_age_group(age):

    if age <= 25:
        return "18-25"

    elif age <= 35:
        return "26-35"

    elif age <= 45:
        return "36-45"

    elif age <= 55:
        return "46-55"

    elif age <= 65:
        return "56-65"

    else:
        return "66+"


df["Age_Group"] = df["Current Age"].apply(
    assign_age_group
)


# ============================================================
# 8. CREATE INCOME GROUP
# ============================================================

def assign_income_group(income):

    if income < 30000:
        return "Low"

    elif income < 60000:
        return "Lower-Middle"

    elif income < 100000:
        return "Upper-Middle"

    else:
        return "High"


df["Income_Group"] = df["Yearly_Income"].apply(
    assign_income_group
)


# ============================================================
# 9. CREATE FICO BAND
# ============================================================

def assign_fico_band(score):

    if score < 580:
        return "Poor"

    elif score < 670:
        return "Fair"

    elif score < 740:
        return "Good"

    elif score < 800:
        return "Very Good"

    else:
        return "Excellent"


df["FICO_Band"] = df["FICO Score"].apply(
    assign_fico_band
)


# ============================================================
# 10. SELECT FINAL COLUMNS
# ============================================================

final_columns = [
    "User_ID",
    "Current Age",
    "Age_Group",
    "Gender",
    "State",
    "Yearly_Income",
    "Income_Group",
    "Total_Debt",
    "FICO Score",
    "FICO_Band",
    "Num Credit Cards"
]

clean_df = df[final_columns].copy()


# ============================================================
# 11. RENAME COLUMNS
# ============================================================

clean_df = clean_df.rename(
    columns={
        "Current Age": "Age",
        "FICO Score": "FICO_Score",
        "Num Credit Cards": "Num_Credit_Cards"
    }
)


# ============================================================
# 12. VALIDATION
# ============================================================

print("\n===== CLEANED DATA VALIDATION =====")

print("Rows:", len(clean_df))
print("Columns:", len(clean_df.columns))

print("\nMissing values:")
print(clean_df.isnull().sum())

print("\nDuplicate rows:")
print(clean_df.duplicated().sum())

print("\nUser_ID unique:")
print(clean_df["User_ID"].nunique())

print("\nAge groups:")
print(clean_df["Age_Group"].value_counts())

print("\nIncome groups:")
print(clean_df["Income_Group"].value_counts())

print("\nFICO bands:")
print(clean_df["FICO_Band"].value_counts())


# ============================================================
# 13. DISPLAY SAMPLE
# ============================================================

print("\n===== CLEANED SAMPLE =====")

print(clean_df.head(10).to_string(index=False))


# ============================================================
# 14. SAVE CLEAN DATA
# ============================================================

clean_df.to_csv(
    output_file,
    index=False
)

print("\nClean customer data saved to:")
print(output_file)

print("\n===== CUSTOMER CLEANING COMPLETE =====")