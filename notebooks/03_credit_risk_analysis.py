import pandas as pd

# Load data
df = pd.read_csv("data/loan_portfolio.csv")

# Create credit score bands
df["credit_score_band"] = pd.cut(
    df["credit_score"],
    bins=[0, 579, 669, 739, 799, 850],
    labels=[
        "Poor (300-579)",
        "Fair (580-669)",
        "Good (670-739)",
        "Very Good (740-799)",
        "Excellent (800-850)"
    ],
    include_lowest=True
)

# Credit score analysis
credit_analysis = (
    df.groupby("credit_score_band", observed=False)
      .agg(
          loans=("loan_id", "count"),
          total_loan_amount=("loan_amount", "sum"),
          defaults=("default_flag", "sum"),
          average_loan_amount=("loan_amount", "mean"),
          average_credit_score=("credit_score", "mean")
      )
      .reset_index()
)

credit_analysis["default_rate"] = (
    credit_analysis["defaults"] / credit_analysis["loans"] * 100
)

print("CREDIT SCORE RISK ANALYSIS")
print("--------------------------")

print("\nDefault Rate by Credit Score Band:")
print(
    credit_analysis[
        [
            "credit_score_band",
            "loans",
            "total_loan_amount",
            "defaults",
            "default_rate"
        ]
    ].to_string(index=False)
)

# DTI bands
df["dti_band"] = pd.cut(
    df["dti_ratio"],
    bins=[0, 0.30, 0.40, 0.50, 0.60, 1.00],
    labels=[
        "Low DTI (<30%)",
        "Moderate DTI (30-40%)",
        "Elevated DTI (40-50%)",
        "High DTI (50-60%)",
        "Very High DTI (>60%)"
    ],
    include_lowest=True
)

dti_analysis = (
    df.groupby("dti_band", observed=False)
      .agg(
          loans=("loan_id", "count"),
          total_loan_amount=("loan_amount", "sum"),
          defaults=("default_flag", "sum")
      )
      .reset_index()
)

dti_analysis["default_rate"] = (
    dti_analysis["defaults"] / dti_analysis["loans"] * 100
)

print("\n\nDEFAULT RATE BY DTI BAND")
print("------------------------")

print(
    dti_analysis[
        [
            "dti_band",
            "loans",
            "total_loan_amount",
            "defaults",
            "default_rate"
        ]
    ].to_string(index=False)
)

# Employment risk
employment_analysis = (
    df.groupby("employment_status")
      .agg(
          loans=("loan_id", "count"),
          total_loan_amount=("loan_amount", "sum"),
          defaults=("default_flag", "sum"),
          average_income=("annual_income", "mean")
      )
      .reset_index()
)

employment_analysis["default_rate"] = (
    employment_analysis["defaults"] / employment_analysis["loans"] * 100
)

print("\n\nDEFAULT RATE BY EMPLOYMENT STATUS")
print("---------------------------------")

print(
    employment_analysis[
        [
            "employment_status",
            "loans",
            "total_loan_amount",
            "defaults",
            "default_rate",
            "average_income"
        ]
    ].to_string(index=False)
)

# Loan purpose risk
purpose_analysis = (
    df.groupby("loan_purpose")
      .agg(
          loans=("loan_id", "count"),
          total_loan_amount=("loan_amount", "sum"),
          defaults=("default_flag", "sum"),
          average_loan_amount=("loan_amount", "mean")
      )
      .reset_index()
)

purpose_analysis["default_rate"] = (
    purpose_analysis["defaults"] / purpose_analysis["loans"] * 100
)

print("\n\nDEFAULT RATE BY LOAN PURPOSE")
print("----------------------------")

print(
    purpose_analysis[
        [
            "loan_purpose",
            "loans",
            "total_loan_amount",
            "defaults",
            "default_rate"
        ]
    ].sort_values("default_rate", ascending=False).to_string(index=False)
)