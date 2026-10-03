import pandas as pd
import numpy as np

# Reproducibility
np.random.seed(42)

# Number of loans
n = 5000

# -----------------------------
# Customer information
# -----------------------------

loan_id = [f"L{i:05d}" for i in range(1, n + 1)]
customer_id = [f"C{i:05d}" for i in np.random.randint(1, 3501, n)]

age = np.random.randint(21, 70, n)

employment_status = np.random.choice(
    ["Employed", "Self-Employed", "Unemployed"],
    size=n,
    p=[0.70, 0.20, 0.10]
)

# Annual income
annual_income = np.random.lognormal(
    mean=np.log(50000),
    sigma=0.45,
    size=n
).round(2)

annual_income = np.clip(annual_income, 18000, 180000)

# Credit score
credit_score = np.random.normal(680, 70, n)
credit_score = np.clip(credit_score, 300, 850).round().astype(int)

# -----------------------------
# Loan information
# -----------------------------

loan_amount = np.random.lognormal(
    mean=np.log(25000),
    sigma=0.65,
    size=n
).round(2)

loan_amount = np.clip(loan_amount, 2000, 150000)

interest_rate = (
    4
    + (700 - credit_score) * 0.025
    + np.random.normal(0, 1, n)
)

interest_rate = np.clip(interest_rate, 3, 18).round(2)

term_months = np.random.choice(
    [12, 24, 36, 48, 60, 72],
    size=n,
    p=[0.08, 0.12, 0.28, 0.20, 0.25, 0.07]
)

loan_purpose = np.random.choice(
    [
        "Home Improvement",
        "Debt Consolidation",
        "Education",
        "Vehicle",
        "Personal"
    ],
    size=n,
    p=[0.15, 0.25, 0.12, 0.23, 0.25]
)

# Debt-to-income ratio
dti_ratio = (
    0.15
    + (loan_amount / annual_income) * 0.45
    + np.random.normal(0, 0.07, n)
)

dti_ratio = np.clip(dti_ratio, 0.05, 0.70).round(3)

# -----------------------------
# Loan origination date
# -----------------------------

origination_date = pd.to_datetime(
    np.random.choice(
        pd.date_range("2023-01-01", "2025-12-31"),
        size=n
    )
)

# -----------------------------
# Default probability
# -----------------------------

# Higher risk from:
# - lower credit score
# - higher DTI
# - unemployment
# - larger loan relative to income

risk_score = (
    -2.2
    + (700 - credit_score) * 0.008
    + (dti_ratio - 0.30) * 2.0
    + (employment_status == "Unemployed") * 0.8
)

default_probability = 1 / (1 + np.exp(-risk_score))

default_flag = np.random.binomial(
    1,
    np.clip(default_probability, 0.02, 0.45)
)

loan_status = np.where(
    default_flag == 1,
    "Default",
    "Active"
)

# -----------------------------
# Create DataFrame
# -----------------------------

df = pd.DataFrame({
    "loan_id": loan_id,
    "customer_id": customer_id,
    "age": age,
    "employment_status": employment_status,
    "annual_income": annual_income,
    "credit_score": credit_score,
    "loan_amount": loan_amount,
    "interest_rate": interest_rate,
    "term_months": term_months,
    "loan_purpose": loan_purpose,
    "dti_ratio": dti_ratio,
    "origination_date": origination_date,
    "default_flag": default_flag,
    "loan_status": loan_status
})

# Sort by origination date
df = df.sort_values("origination_date").reset_index(drop=True)

# Save
output_path = "data/loan_portfolio.csv"
df.to_csv(output_path, index=False)

# -----------------------------
# Basic checks
# -----------------------------

print("LOAN DATASET CREATED")
print("--------------------")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"File: {output_path}")

print("\nLoan Status:")
print(df["loan_status"].value_counts())

print("\nDefault Rate:")
print(f"{df['default_flag'].mean() * 100:.2f}%")

print("\nTotal Loan Amount:")
print(f"€{df['loan_amount'].sum():,.2f}")

print("\nAverage Credit Score:")
print(f"{df['credit_score'].mean():.2f}")

print("\nMissing Values:")
print(df.isnull().sum().sum())