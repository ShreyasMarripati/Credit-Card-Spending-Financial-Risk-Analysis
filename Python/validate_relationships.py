import pandas as pd

# ============================================================
# 1. LOAD THE THREE DATASETS
# ============================================================

users_file = "../data/raw/sd254_users.csv"
cards_file = "../data/raw/sd254_cards.csv"
transactions_file = "../data/raw/credit_card_transactions_project.csv"

users = pd.read_csv(users_file)
cards = pd.read_csv(cards_file)
transactions = pd.read_csv(transactions_file)


# ============================================================
# 2. BASIC INFORMATION
# ============================================================

print("============================================================")
print("RELATIONSHIP VALIDATION")
print("============================================================")

print("\n===== DATASET SIZES =====")

print("Customers:", len(users))
print("Cards:", len(cards))
print("Transactions:", len(transactions))


# ============================================================
# 3. CUSTOMER USER ID VALIDATION
# ============================================================

print("\n===== CUSTOMER USER ID RANGE =====")

print("Expected User IDs:")
print("0 to", len(users) - 1)

print("\nTransaction User range:")
print("Minimum:", transactions["User"].min())
print("Maximum:", transactions["User"].max())

print("\nCard User range:")
print("Minimum:", cards["User"].min())
print("Maximum:", cards["User"].max())


# ============================================================
# 4. CHECK TRANSACTION USERS AGAINST CUSTOMERS
# ============================================================

print("\n===== TRANSACTION → CUSTOMER VALIDATION =====")

customer_ids = set(range(len(users)))

transaction_users = set(transactions["User"].unique())

invalid_transaction_users = transaction_users - customer_ids

print("Unique transaction users:",
      len(transaction_users))

print("Invalid transaction users:",
      len(invalid_transaction_users))

if len(invalid_transaction_users) == 0:
    print("RESULT: All transaction users match customers.")
else:
    print("Invalid User IDs:")
    print(sorted(invalid_transaction_users)[:20])


# ============================================================
# 5. CHECK CARD USERS AGAINST CUSTOMERS
# ============================================================

print("\n===== CARD → CUSTOMER VALIDATION =====")

card_users = set(cards["User"].unique())

invalid_card_users = card_users - customer_ids

print("Unique card users:",
      len(card_users))

print("Invalid card users:",
      len(invalid_card_users))

if len(invalid_card_users) == 0:
    print("RESULT: All card users match customers.")
else:
    print("Invalid User IDs:")
    print(sorted(invalid_card_users)[:20])


# ============================================================
# 6. CREATE CARD KEY
# ============================================================

print("\n===== CARD KEY VALIDATION =====")

cards["Card_ID"] = (
    cards["User"].astype(str)
    + "_"
    + cards["CARD INDEX"].astype(str)
)

print("Total card records:",
      len(cards))

print("Unique Card_ID values:",
      cards["Card_ID"].nunique())

duplicate_card_ids = (
    cards["Card_ID"].duplicated().sum()
)

print("Duplicate Card_ID values:",
      duplicate_card_ids)


# ============================================================
# 7. CREATE TRANSACTION CARD KEY
# ============================================================

transactions["Card_ID"] = (
    transactions["User"].astype(str)
    + "_"
    + transactions["Card"].astype(str)
)


# ============================================================
# 8. CHECK TRANSACTION CARDS AGAINST CARD DATASET
# ============================================================

print("\n===== TRANSACTION → CARD VALIDATION =====")

valid_card_ids = set(cards["Card_ID"])

transaction_card_ids = set(
    transactions["Card_ID"].unique()
)

invalid_transaction_cards = (
    transaction_card_ids - valid_card_ids
)

print("Unique transaction Card_IDs:",
      len(transaction_card_ids))

print("Invalid transaction Card_IDs:",
      len(invalid_transaction_cards))

if len(invalid_transaction_cards) == 0:
    print("RESULT: All transaction cards match card records.")
else:
    print("Some transaction cards do not exist in card dataset.")

    print("\nFirst 20 invalid Card_IDs:")
    print(sorted(invalid_transaction_cards)[:20])


# ============================================================
# 9. CHECK HOW MANY TRANSACTIONS MATCH A CARD
# ============================================================

print("\n===== TRANSACTION CARD MATCH RATE =====")

transactions["Card_Match"] = (
    transactions["Card_ID"].isin(valid_card_ids)
)

matched_transactions = transactions["Card_Match"].sum()

unmatched_transactions = (
    (~transactions["Card_Match"]).sum()
)

print("Matched transactions:",
      matched_transactions)

print("Unmatched transactions:",
      unmatched_transactions)

match_rate = (
    matched_transactions / len(transactions)
) * 100

print("Match rate:",
      round(match_rate, 2), "%")


# ============================================================
# 10. CHECK TRANSACTION USERS AGAINST CARD USERS
# ============================================================

print("\n===== TRANSACTION USER → CARD USER VALIDATION =====")

transaction_user_set = set(transactions["User"].unique())

invalid_users_against_cards = (
    transaction_user_set - card_users
)

print("Transaction users without cards:",
      len(invalid_users_against_cards))

if len(invalid_users_against_cards) == 0:
    print("RESULT: Every transaction user has at least one card.")
else:
    print("Users without card records:")
    print(sorted(invalid_users_against_cards)[:20])


# ============================================================
# 11. SUMMARY
# ============================================================

print("\n============================================================")
print("VALIDATION SUMMARY")
print("============================================================")

print("Customers:", len(users))
print("Cards:", len(cards))
print("Transactions:", len(transactions))

print("\nTransaction users matched to customers:",
      len(invalid_transaction_users) == 0)

print("Card users matched to customers:",
      len(invalid_card_users) == 0)

print("Card IDs unique:",
      duplicate_card_ids == 0)

print("Transaction cards matched to cards:",
      len(invalid_transaction_cards) == 0)

print("Every transaction user has a card:",
      len(invalid_users_against_cards) == 0)

print("\n===== RELATIONSHIP VALIDATION COMPLETE =====")