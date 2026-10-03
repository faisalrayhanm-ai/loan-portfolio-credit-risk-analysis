# Loan Portfolio & Credit Risk Analysis

## Project Overview

This project analyses a synthetic loan portfolio to understand credit risk, borrower characteristics, loan exposure, and default patterns.

The analysis was performed using Python, SQL, Excel, and Power BI.

## Business Objectives

- Analyse the overall loan portfolio
- Measure loan amounts and credit quality
- Analyse default rates by credit score
- Analyse default rates by debt-to-income ratio
- Compare default rates across employment status
- Analyse default rates by loan purpose
- Segment loans into simple risk categories
- Build an interactive Power BI dashboard

## Dataset

The dataset contains 5,000 synthetic loan records.

Key fields include:

- Loan ID
- Customer ID
- Age
- Employment Status
- Annual Income
- Credit Score
- Loan Amount
- Interest Rate
- Term
- Loan Purpose
- Debt-to-Income Ratio
- Origination Date
- Default Flag
- Loan Status

The dataset is synthetic and was created specifically for this portfolio project. It does not contain real customer or bank information.

## Key Portfolio Metrics

- Total Loans: 5,000
- Total Loan Amount: €155.14 million
- Average Loan Amount: €31,028.82
- Average Credit Score: 680.82
- Average DTI: 41.59%
- Default Rate: 16.74%

## Analysis Performed

### Credit Score Analysis

Default rates were compared across:

- Poor
- Fair
- Good
- Very Good
- Excellent

The analysis showed higher observed default rates among lower credit-score groups in this synthetic dataset.

### DTI Analysis

Loans were grouped by debt-to-income ratio:

- Low DTI
- Moderate DTI
- Elevated DTI
- High DTI
- Very High DTI

Higher DTI groups showed higher observed default rates in the synthetic portfolio.

### Employment Analysis

Default rates were compared across:

- Employed
- Self-Employed
- Unemployed

The unemployed group had the highest observed default rate in this synthetic dataset.

### Loan Purpose Analysis

Default rates were compared across:

- Personal
- Vehicle
- Debt Consolidation
- Home Improvement
- Education

## Risk Segmentation

A simple analytical risk segmentation was created using credit score and DTI:

- High Risk
- Medium Risk
- Low Risk

This segmentation is an analytical portfolio classification and is not a machine-learning credit approval model.

## Tools Used

- Python
- Pandas
- NumPy
- SQL
- SQLite
- SQLAlchemy
- Excel
- Power BI

## Project Workflow

1. Generated synthetic loan data using Python
2. Performed data quality checks
3. Calculated portfolio KPIs
4. Analysed credit risk characteristics
5. Created risk segments
6. Loaded the dataset into SQLite
7. Performed SQL analysis
8. Created an Excel dashboard
9. Built an interactive Power BI dashboard

## Power BI Dashboard

The dashboard includes:

- Total Loans
- Total Loan Amount
- Overall Default Rate
- Default Rate by Credit Score
- Default Rate by DTI
- Default Rate by Employment Status
- Default Rate by Loan Purpose

## Important Note

The dataset is synthetic. The findings describe patterns within this generated dataset and should not be interpreted as real-world banking statistics or causal relationships.