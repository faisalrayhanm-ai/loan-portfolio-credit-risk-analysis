import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///data/loan_portfolio.db")

# --------------------------------------------------
# 1. Portfolio KPIs
# --------------------------------------------------

query = """
SELECT
    COUNT(loan_id) AS total_loans,
    SUM(loan_amount) AS total_loan_amount,
    AVG(loan_amount) AS average_loan_amount,
    AVG(credit_score) AS average_credit_score,
    AVG(dti_ratio) AS average_dti,
    SUM(default_flag) AS total_defaults,
    AVG(default_flag) * 100 AS default_rate
FROM loan_portfolio;
"""

result = pd.read_sql(query, engine)

print("PORTFOLIO KPIs")
print("--------------")
print(result.to_string(index=False))


# --------------------------------------------------
# 2. Default rate by credit score band
# --------------------------------------------------

query = """
SELECT
    CASE
        WHEN credit_score < 580 THEN 'Poor'
        WHEN credit_score < 670 THEN 'Fair'
        WHEN credit_score < 740 THEN 'Good'
        WHEN credit_score < 800 THEN 'Very Good'
        ELSE 'Excellent'
    END AS credit_score_band,
    COUNT(loan_id) AS loans,
    SUM(loan_amount) AS total_loan_amount,
    SUM(default_flag) AS defaults,
    AVG(default_flag) * 100 AS default_rate
FROM loan_portfolio
GROUP BY credit_score_band
ORDER BY default_rate DESC;
"""

result = pd.read_sql(query, engine)

print("\n\nDEFAULT RATE BY CREDIT SCORE")
print("----------------------------")
print(result.to_string(index=False))


# --------------------------------------------------
# 3. Default rate by loan purpose
# --------------------------------------------------

query = """
SELECT
    loan_purpose,
    COUNT(loan_id) AS loans,
    SUM(loan_amount) AS total_loan_amount,
    SUM(default_flag) AS defaults,
    AVG(default_flag) * 100 AS default_rate
FROM loan_portfolio
GROUP BY loan_purpose
ORDER BY default_rate DESC;
"""

result = pd.read_sql(query, engine)

print("\n\nDEFAULT RATE BY LOAN PURPOSE")
print("----------------------------")
print(result.to_string(index=False))


# --------------------------------------------------
# 4. Employment risk analysis
# --------------------------------------------------

query = """
SELECT
    employment_status,
    COUNT(loan_id) AS loans,
    SUM(loan_amount) AS total_loan_amount,
    SUM(default_flag) AS defaults,
    AVG(default_flag) * 100 AS default_rate,
    AVG(annual_income) AS average_income
FROM loan_portfolio
GROUP BY employment_status
ORDER BY default_rate DESC;
"""

result = pd.read_sql(query, engine)

print("\n\nDEFAULT RATE BY EMPLOYMENT")
print("--------------------------")
print(result.to_string(index=False))


# --------------------------------------------------
# 5. DTI risk analysis
# --------------------------------------------------

query = """
SELECT
    CASE
        WHEN dti_ratio < 0.30 THEN 'Low DTI'
        WHEN dti_ratio < 0.40 THEN 'Moderate DTI'
        WHEN dti_ratio < 0.50 THEN 'Elevated DTI'
        WHEN dti_ratio < 0.60 THEN 'High DTI'
        ELSE 'Very High DTI'
    END AS dti_band,
    COUNT(loan_id) AS loans,
    SUM(loan_amount) AS total_loan_amount,
    SUM(default_flag) AS defaults,
    AVG(default_flag) * 100 AS default_rate
FROM loan_portfolio
GROUP BY dti_band
ORDER BY default_rate DESC;
"""

result = pd.read_sql(query, engine)

print("\n\nDEFAULT RATE BY DTI")
print("-------------------")
print(result.to_string(index=False))