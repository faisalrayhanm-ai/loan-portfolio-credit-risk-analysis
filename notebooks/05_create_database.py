import pandas as pd
from sqlalchemy import create_engine

# Load loan data
df = pd.read_csv("data/loan_portfolio.csv")

# Convert date
df["origination_date"] = pd.to_datetime(df["origination_date"])

# Create SQLite database
engine = create_engine("sqlite:///data/loan_portfolio.db")

# Write data to database
df.to_sql(
    "loan_portfolio",
    engine,
    if_exists="replace",
    index=False
)

print("SQL DATABASE CREATED")
print("--------------------")
print("Database: data/loan_portfolio.db")
print(f"Rows inserted: {len(df):,}")