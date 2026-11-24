import pandas as pd


# ============================================================
# 1. FILE PATHS
# ============================================================

customers_file = "../data/processed/clean_customers.csv"
cards_file = "../data/processed/clean_cards.csv"
transactions_file = "../data/processed/clean_transactions.csv"


# ============================================================
# 2. LOAD CLEANED DATA
# ============================================================

customers = pd.read_csv(customers_file)
cards = pd.read_csv(cards_file)
transactions = pd.read_csv(transactions_file)


print("============================================================")
print("FINAL CLEAN DATA VALIDATION")
print("============================================================")


# ============================================================
# 3. DATASET SIZES
# ============================================================

print("\n===== DATASET SIZES =====")

print("Customers:", len(customers))
print("Cards:", len(cards))
print("Transactions:", len(transactions))


# ============================================================
# 4. CUSTOMER ID VALIDATION
# ============================================================

print("\n===== CUSTOMER ID VALIDATION =====")

customer_ids = set(customers["User_ID"])

print("Customer records:", len(customers))
print("Unique User_IDs:", customers["User_ID"].nunique())

invalid_card_users = (
    set(cards["User_ID"]) - customer_ids
)

invalid_transaction_users = (
    set(transactions["User_ID"]) - customer_ids
)

print(
    "Card users not found in customers:",
    len(invalid_card_users)
)

print(
    "Transaction users not found in customers:",
    len(invalid_transaction_users)
)


# ============================================================
# 5. CARD ID VALIDATION
# ============================================================

print("\n===== CARD ID VALIDATION =====")

card_ids = set(cards["Card_ID"])

print("Card records:", len(cards))
print("Unique Card_IDs:", cards["Card_ID"].nunique())

duplicate_card_ids = (
    cards["Card_ID"].duplicated().sum()
)

print(
    "Duplicate Card_IDs:",
    duplicate_card_ids
)


# ============================================================
# 6. TRANSACTION → CARD VALIDATION
# ============================================================

print("\n===== TRANSACTION → CARD VALIDATION =====")

transaction_card_ids = set(
    transactions["Card_ID"]
)

invalid_transaction_cards = (
    transaction_card_ids - card_ids
)

print(
    "Unique transaction Card_IDs:",
    len(transaction_card_ids)
)

print(
    "Transaction Card_IDs not found in cards:",
    len(invalid_transaction_cards)
)

matched_transactions = (
    transactions["Card_ID"].isin(card_ids).sum()
)

print(
    "Transactions matched to cards:",
    matched_transactions
)

print(
    "Transactions not matched to cards:",
    len(transactions) - matched_transactions
)


# ============================================================
# 7. TRANSACTION → CUSTOMER VALIDATION
# ============================================================

print("\n===== TRANSACTION → CUSTOMER VALIDATION =====")

matched_transaction_users = (
    transactions["User_ID"].isin(customer_ids).sum()
)

print(
    "Transactions matched to customers:",
    matched_transaction_users
)

print(
    "Transactions not matched to customers:",
    len(transactions) - matched_transaction_users
)


# ============================================================
# 8. TRANSACTION ID VALIDATION
# ============================================================

print("\n===== TRANSACTION ID VALIDATION =====")

print(
    "Transaction records:",
    len(transactions)
)

print(
    "Unique Transaction_IDs:",
    transactions["Transaction_ID"].nunique()
)

print(
    "Duplicate Transaction_IDs:",
    transactions["Transaction_ID"].duplicated().sum()
)


# ============================================================
# 9. FRAUD COUNT VALIDATION
# ============================================================

print("\n===== FRAUD VALIDATION =====")

fraud_count = (
    transactions["Fraud_Flag"] == 1
).sum()

print(
    "Fraud transactions:",
    fraud_count
)


# ============================================================
# 10. ERROR COUNT VALIDATION
# ============================================================

print("\n===== ERROR VALIDATION =====")

error_count = (
    transactions["Error_Flag"] == 1
).sum()

print(
    "Transactions with errors:",
    error_count
)


# ============================================================
# 11. AMOUNT VALIDATION
# ============================================================

print("\n===== AMOUNT VALIDATION =====")

print(
    "Total transaction amount:",
    round(transactions["Amount"].sum(), 2)
)

print(
    "Minimum transaction amount:",
    transactions["Amount"].min()
)

print(
    "Maximum transaction amount:",
    transactions["Amount"].max()
)


# ============================================================
# 12. CARD TYPE VALIDATION
# ============================================================

print("\n===== CARD TYPE VALIDATION =====")

print(
    cards["Card_Type"].value_counts()
)


# ============================================================
# 13. CARDS ISSUED VS CUSTOMER CREDIT CARDS
# ============================================================

print("\n===== CARDS ISSUED VS CUSTOMER CARD COUNT =====")

card_count_by_user = (
    cards.groupby("User_ID")
    .size()
    .reset_index(name="Actual_Card_Count")
)

comparison = customers[
    ["User_ID", "Num_Credit_Cards"]
].merge(
    card_count_by_user,
    on="User_ID",
    how="left"
)

comparison["Difference"] = (
    comparison["Num_Credit_Cards"]
    - comparison["Actual_Card_Count"]
)

print(
    comparison["Difference"].value_counts()
)

print(
    "\nCustomers where Num_Credit_Cards "
    "does not equal actual card count:"
)

print(
    (comparison["Difference"] != 0).sum()
)


# ============================================================
# 14. CHECK MISSING VALUES
# ============================================================

print("\n===== FINAL MISSING VALUE CHECK =====")

print("\nCustomers:")
print(customers.isnull().sum())

print("\nCards:")
print(cards.isnull().sum())

print("\nTransactions:")
print(transactions.isnull().sum())


# ============================================================
# 15. FINAL SUMMARY
# ============================================================

print("\n============================================================")
print("FINAL VALIDATION SUMMARY")
print("============================================================")

print(
    "Customer rows correct:",
    len(customers) == 2000
)

print(
    "Card rows correct:",
    len(cards) == 6146
)

print(
    "Transaction rows correct:",
    len(transactions) == 300000
)

print(
    "Customer IDs unique:",
    customers["User_ID"].nunique() == len(customers)
)

print(
    "Card IDs unique:",
    cards["Card_ID"].nunique() == len(cards)
)

print(
    "Transaction IDs unique:",
    transactions["Transaction_ID"].nunique()
    == len(transactions)
)

print(
    "All card users valid:",
    len(invalid_card_users) == 0
)

print(
    "All transaction users valid:",
    len(invalid_transaction_users) == 0
)

print(
    "All transaction cards valid:",
    len(invalid_transaction_cards) == 0
)

print(
    "All transactions matched to cards:",
    matched_transactions == len(transactions)
)

print(
    "All transactions matched to customers:",
    matched_transaction_users == len(transactions)
)


# ============================================================
# COMPLETE
# ============================================================

print("\n===== FINAL CLEAN DATA VALIDATION COMPLETE =====")