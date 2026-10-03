import pandas as pd

# Load data
df = pd.read_csv("data/loan_portfolio.csv")

# Credit score band
df["credit_score_band"] = pd.cut(
    df["credit_score"],
    bins=[0, 579, 669, 739, 799, 850],
    labels=[
        "Poor",
        "Fair",
        "Good",
        "Very Good",
        "Excellent"
    ],
    include_lowest=True
)

# Create risk segment
def classify_risk(row):

    if row["credit_score"] < 580 or row["dti_ratio"] > 0.60:
        return "High Risk"

    elif row["credit_score"] < 670 or row["dti_ratio"] > 0.50:
        return "Medium Risk"

    else:
        return "Low Risk"


df["risk_segment"] = df.apply(classify_risk, axis=1)

# Analyse risk segments
risk_analysis = (
    df.groupby("risk_segment")
      .agg(
          loans=("loan_id", "count"),
          total_loan_amount=("loan_amount", "sum"),
          defaults=("default_flag", "sum"),
          average_loan_amount=("loan_amount", "mean"),
          average_credit_score=("credit_score", "mean"),
          average_dti=("dti_ratio", "mean")
      )
      .reset_index()
)

risk_analysis["default_rate"] = (
    risk_analysis["defaults"] /
    risk_analysis["loans"] * 100
)

# Order segments
risk_order = ["Low Risk", "Medium Risk", "High Risk"]

risk_analysis["risk_segment"] = pd.Categorical(
    risk_analysis["risk_segment"],
    categories=risk_order,
    ordered=True
)

risk_analysis = risk_analysis.sort_values("risk_segment")

print("LOAN PORTFOLIO RISK SEGMENTATION")
print("--------------------------------")

print(
    risk_analysis[
        [
            "risk_segment",
            "loans",
            "total_loan_amount",
            "defaults",
            "default_rate",
            "average_loan_amount",
            "average_credit_score",
            "average_dti"
        ]
    ].to_string(index=False)
)

# Risk distribution
print("\nRISK SEGMENT DISTRIBUTION")
print("-------------------------")

print(
    df["risk_segment"]
    .value_counts()
    .reindex(risk_order)
)

# Cross-check overall default rate
print("\nOVERALL DEFAULT RATE")
print("--------------------")
print(f"{df['default_flag'].mean() * 100:.2f}%")