USE credit_card_finance;

CREATE OR REPLACE VIEW vw_customer_spending AS
SELECT
    f.User_ID,

    COUNT(*) AS Transaction_Count,

    ROUND(
        SUM(
            CASE
                WHEN f.Amount > 0 THEN f.Amount
                ELSE 0
            END
        ),
        2
    ) AS Gross_Spending,

    ROUND(
        SUM(f.Amount),
        2
    ) AS Net_Spending,

    ROUND(
        AVG(f.Amount),
        2
    ) AS Average_Transaction,

    ROUND(
        MAX(f.Amount),
        2
    ) AS Largest_Transaction,

    SUM(
        CASE
            WHEN f.Transaction_Channel = 'Online' THEN 1
            ELSE 0
        END
    ) AS Online_Transactions,

    SUM(
        CASE
            WHEN f.Transaction_Channel = 'Chip' THEN 1
            ELSE 0
        END
    ) AS Chip_Transactions,

    SUM(
        CASE
            WHEN f.Transaction_Channel = 'Swipe' THEN 1
            ELSE 0
        END
    ) AS Swipe_Transactions,

    SUM(
        CASE
            WHEN f.Fraud_Flag = 1 THEN 1
            ELSE 0
        END
    ) AS Fraud_Transactions,

    SUM(
        CASE
            WHEN f.Error_Flag = 1 THEN 1
            ELSE 0
        END
    ) AS Error_Transactions

FROM fact_transactions f

GROUP BY f.User_ID;