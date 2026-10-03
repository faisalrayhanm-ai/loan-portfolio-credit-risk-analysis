import pandas as pd

# Load data
df = pd.read_csv("data/loan_portfolio.csv")

# Convert date
df["origination_date"] = pd.to_datetime(df["origination_date"])

print("LOAN PORTFOLIO ANALYSIS")
print("----------------------")

# Dataset information
print("\nDataset Shape:")
print(df.shape)

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Portfolio KPIs
total_loans = len(df)
total_loan_amount = df["loan_amount"].sum()
average_loan_amount = df["loan_amount"].mean()
average_credit_score = df["credit_score"].mean()
average_dti = df["dti_ratio"].mean()
default_rate = df["default_flag"].mean() * 100

print("\nPORTFOLIO KPIs")
print("--------------")
print(f"Total Loans: {total_loans:,}")
print(f"Total Loan Amount: €{total_loan_amount:,.2f}")
print(f"Average Loan Amount: €{average_loan_amount:,.2f}")
print(f"Average Credit Score: {average_credit_score:.2f}")
print(f"Average DTI Ratio: {average_dti:.2%}")
print(f"Default Rate: {default_rate:.2f}%")

# Loan status
print("\nLoan Status:")
print(df["loan_status"].value_counts())

# Employment status
print("\nEmployment Status:")
print(df["employment_status"].value_counts())

# Loan purpose
print("\nLoan Purpose:")
print(df["loan_purpose"].value_counts())

# Credit score statistics
print("\nCredit Score Statistics:")
print(df["credit_score"].describe())

# Loan amount statistics
print("\nLoan Amount Statistics:")
print(df["loan_amount"].describe())

# DTI statistics
print("\nDTI Statistics:")
print(df["dti_ratio"].describe())