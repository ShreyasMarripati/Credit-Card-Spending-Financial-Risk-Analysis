import pandas as pd
import os

# ============================================================
# FILE PATHS
# ============================================================

input_file = "../data/processed/clean_transactions.csv"
output_file = "../data/processed/dim_date.csv"

# ============================================================
# LOAD TRANSACTIONS
# ============================================================

df = pd.read_csv(input_file)

print("Transactions Loaded:", len(df))

# ============================================================
# CONVERT TRANSACTION DATE
# ============================================================

df["Transaction_Date"] = pd.to_datetime(
    df["Transaction_Date"]
)

# ============================================================
# FIND DATE RANGE
# ============================================================

start_date = df["Transaction_Date"].min()
end_date = df["Transaction_Date"].max()

print("\nDate Range:")
print("Start:", start_date)
print("End:", end_date)

# ============================================================
# GENERATE COMPLETE DATE RANGE
# ============================================================

dates = pd.date_range(
    start=start_date,
    end=end_date,
    freq="D"
)

# ============================================================
# CREATE DATE DIMENSION
# ============================================================

date_df = pd.DataFrame({
    "Date": dates
})

# ============================================================
# CREATE DATE KEY
# ============================================================

date_df["Date_ID"] = (
    date_df["Date"].dt.strftime("%Y%m%d").astype(int)
)

# ============================================================
# CREATE CALENDAR ATTRIBUTES
# ============================================================

date_df["Year"] = date_df["Date"].dt.year

date_df["Quarter"] = (
    date_df["Date"].dt.quarter
)

date_df["Month"] = (
    date_df["Date"].dt.month
)

date_df["Month_Name"] = (
    date_df["Date"].dt.strftime("%B")
)

date_df["Month_Number"] = (
    date_df["Date"].dt.month
)

date_df["Day"] = (
    date_df["Date"].dt.day
)

date_df["Day_Name"] = (
    date_df["Date"].dt.strftime("%A")
)

# ============================================================
# REORDER COLUMNS
# ============================================================

date_df = date_df[
    [
        "Date_ID",
        "Date",
        "Year",
        "Quarter",
        "Month",
        "Month_Name",
        "Month_Number",
        "Day",
        "Day_Name"
    ]
]

# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("DATE DIMENSION VALIDATION")
print("=" * 60)

print("\nDate rows:", len(date_df))

print("\nMissing Values:")
print(date_df.isnull().sum())

print(
    "\nDuplicate Date_IDs:",
    date_df["Date_ID"].duplicated().sum()
)

print(
    "Unique Date_IDs:",
    date_df["Date_ID"].nunique()
)

print("\nSample:")
print(
    date_df.head(10).to_string(index=False)
)

print("\nLast 5 dates:")
print(
    date_df.tail(5).to_string(index=False)
)

# ============================================================
# SAVE
# ============================================================

date_df.to_csv(
    output_file,
    index=False
)

print("\nDate dimension saved to:")
print(output_file)

print("\n===== DIM_DATE CREATED SUCCESSFULLY =====")