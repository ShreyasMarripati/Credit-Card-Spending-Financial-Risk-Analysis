USE credit_card_finance;

CREATE OR REPLACE VIEW vw_customer_risk AS
SELECT
    User_ID,
    Age,
    Age_Group,
    Gender,
    State,
    Yearly_Income,
    Income_Group,
    Total_Debt,
    Debt_to_Income_Ratio,
    DTI_Band,
    FICO_Score,
    FICO_Band,
    Num_Credit_Cards,

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
    END AS Risk_Level

FROM vw_customer_financial_profile;

SELECT *
FROM vw_customer_risk
LIMIT 20;
SELECT COUNT(*) AS Customer_Count
FROM vw_customer_risk;
SELECT
    Risk_Level,
    COUNT(*) AS Customer_Count
FROM vw_customer_risk
GROUP BY Risk_Level
ORDER BY
    CASE Risk_Level
        WHEN 'Low Risk' THEN 1
        WHEN 'Medium Risk' THEN 2
        WHEN 'High Risk' THEN 3
    END;