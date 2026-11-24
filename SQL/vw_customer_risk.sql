USE credit_card_finance;

SELECT
    CASE
        WHEN FICO_Band IN ('Excellent', 'Very Good')
            THEN 0
        WHEN FICO_Band = 'Good'
            THEN 1
        WHEN FICO_Band = 'Fair'
            THEN 2
        WHEN FICO_Band = 'Poor'
            THEN 3
    END
    +
    CASE
        WHEN Debt_to_Income_Ratio < 36
            THEN 0
        WHEN Debt_to_Income_Ratio < 50
            THEN 1
        WHEN Debt_to_Income_Ratio < 100
            THEN 2
        ELSE 3
    END AS Risk_Score,

    COUNT(*) AS Customer_Count

FROM vw_customer_financial_profile

GROUP BY
    CASE
        WHEN FICO_Band IN ('Excellent', 'Very Good')
            THEN 0
        WHEN FICO_Band = 'Good'
            THEN 1
        WHEN FICO_Band = 'Fair'
            THEN 2
        WHEN FICO_Band = 'Poor'
            THEN 3
    END
    +
    CASE
        WHEN Debt_to_Income_Ratio < 36
            THEN 0
        WHEN Debt_to_Income_Ratio < 50
            THEN 1
        WHEN Debt_to_Income_Ratio < 100
            THEN 2
        ELSE 3
    END

ORDER BY Risk_Score;
SELECT
    CASE
        WHEN
            (
                CASE
                    WHEN FICO_Band IN ('Excellent', 'Very Good') THEN 0
                    WHEN FICO_Band = 'Good' THEN 1
                    WHEN FICO_Band = 'Fair' THEN 2
                    WHEN FICO_Band = 'Poor' THEN 3
                END
                +
                CASE
                    WHEN Debt_to_Income_Ratio < 36 THEN 0
                    WHEN Debt_to_Income_Ratio < 50 THEN 1
                    WHEN Debt_to_Income_Ratio < 100 THEN 2
                    ELSE 3
                END
            ) <= 1
            THEN 'Low Risk'

        WHEN
            (
                CASE
                    WHEN FICO_Band IN ('Excellent', 'Very Good') THEN 0
                    WHEN FICO_Band = 'Good' THEN 1
                    WHEN FICO_Band = 'Fair' THEN 2
                    WHEN FICO_Band = 'Poor' THEN 3
                END
                +
                CASE
                    WHEN Debt_to_Income_Ratio < 36 THEN 0
                    WHEN Debt_to_Income_Ratio < 50 THEN 1
                    WHEN Debt_to_Income_Ratio < 100 THEN 2
                    ELSE 3
                END
            ) <= 3
            THEN 'Medium Risk'

        ELSE 'High Risk'
    END AS Risk_Level,

    COUNT(*) AS Customer_Count

FROM vw_customer_financial_profile

GROUP BY
    CASE
        WHEN
            (
                CASE
                    WHEN FICO_Band IN ('Excellent', 'Very Good') THEN 0
                    WHEN FICO_Band = 'Good' THEN 1
                    WHEN FICO_Band = 'Fair' THEN 2
                    WHEN FICO_Band = 'Poor' THEN 3
                END
                +
                CASE
                    WHEN Debt_to_Income_Ratio < 36 THEN 0
                    WHEN Debt_to_Income_Ratio < 50 THEN 1
                    WHEN Debt_to_Income_Ratio < 100 THEN 2
                    ELSE 3
                END
            ) <= 1
            THEN 'Low Risk'

        WHEN
            (
                CASE
                    WHEN FICO_Band IN ('Excellent', 'Very Good') THEN 0
                    WHEN FICO_Band = 'Good' THEN 1
                    WHEN FICO_Band = 'Fair' THEN 2
                    WHEN FICO_Band = 'Poor' THEN 3
                END
                +
                CASE
                    WHEN Debt_to_Income_Ratio < 36 THEN 0
                    WHEN Debt_to_Income_Ratio < 50 THEN 1
                    WHEN Debt_to_Income_Ratio < 100 THEN 2
                    ELSE 3
                END
            ) <= 3
            THEN 'Medium Risk'

        ELSE 'High Risk'
    END;