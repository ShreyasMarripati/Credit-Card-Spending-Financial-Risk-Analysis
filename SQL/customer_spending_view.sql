SELECT *
FROM vw_customer_spending
LIMIT 20;
SELECT COUNT(*) AS Customer_Count
FROM vw_customer_spending;
SELECT
    User_ID,
    Transaction_Count,
    Gross_Spending,
    Net_Spending,
    Average_Transaction,
    Largest_Transaction
FROM vw_customer_spending
ORDER BY Gross_Spending DESC
LIMIT 10;