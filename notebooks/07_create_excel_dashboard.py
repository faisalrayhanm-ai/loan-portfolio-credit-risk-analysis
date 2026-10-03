import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.utils import get_column_letter

# --------------------------------------------------
# Load data
# --------------------------------------------------

df = pd.read_csv("data/loan_portfolio.csv")

# --------------------------------------------------
# Create analysis tables
# --------------------------------------------------

# Portfolio KPIs
total_loans = len(df)
total_loan_amount = df["loan_amount"].sum()
average_loan_amount = df["loan_amount"].mean()
average_credit_score = df["credit_score"].mean()
default_rate = df["default_flag"].mean()

# Credit score analysis
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

credit_analysis = (
    df.groupby("credit_score_band", observed=False)
    .agg(
        Loans=("loan_id", "count"),
        Total_Loan_Amount=("loan_amount", "sum"),
        Defaults=("default_flag", "sum")
    )
    .reset_index()
)

credit_analysis["Default_Rate"] = (
    credit_analysis["Defaults"] /
    credit_analysis["Loans"]
)

# DTI analysis
df["dti_band"] = pd.cut(
    df["dti_ratio"],
    bins=[0, 0.30, 0.40, 0.50, 0.60, 1.00],
    labels=[
        "Low DTI",
        "Moderate DTI",
        "Elevated DTI",
        "High DTI",
        "Very High DTI"
    ],
    include_lowest=True
)

dti_analysis = (
    df.groupby("dti_band", observed=False)
    .agg(
        Loans=("loan_id", "count"),
        Total_Loan_Amount=("loan_amount", "sum"),
        Defaults=("default_flag", "sum")
    )
    .reset_index()
)

dti_analysis["Default_Rate"] = (
    dti_analysis["Defaults"] /
    dti_analysis["Loans"]
)

# Employment analysis
employment_analysis = (
    df.groupby("employment_status")
    .agg(
        Loans=("loan_id", "count"),
        Total_Loan_Amount=("loan_amount", "sum"),
        Defaults=("default_flag", "sum")
    )
    .reset_index()
)

employment_analysis["Default_Rate"] = (
    employment_analysis["Defaults"] /
    employment_analysis["Loans"]
)

# Loan purpose analysis
purpose_analysis = (
    df.groupby("loan_purpose")
    .agg(
        Loans=("loan_id", "count"),
        Total_Loan_Amount=("loan_amount", "sum"),
        Defaults=("default_flag", "sum")
    )
    .reset_index()
)

purpose_analysis["Default_Rate"] = (
    purpose_analysis["Defaults"] /
    purpose_analysis["Loans"]
)

# --------------------------------------------------
# Create workbook
# --------------------------------------------------

wb = Workbook()

# Remove default sheet
ws = wb.active
ws.title = "Dashboard"

# --------------------------------------------------
# Dashboard
# --------------------------------------------------

ws["A1"] = "Loan Portfolio & Credit Risk Analysis"
ws["A1"].font = Font(size=18, bold=True)

ws["A3"] = "Total Loans"
ws["B3"] = total_loans

ws["D3"] = "Total Loan Amount"
ws["E3"] = total_loan_amount

ws["G3"] = "Average Loan Amount"
ws["H3"] = average_loan_amount

ws["J3"] = "Default Rate"
ws["K3"] = default_rate

for cell in ["A3", "D3", "G3", "J3"]:
    ws[cell].font = Font(bold=True)

for cell in ["B3", "E3", "H3", "K3"]:
    ws[cell].font = Font(size=14, bold=True)

ws["E3"].number_format = '€#,##0.00'
ws["H3"].number_format = '€#,##0.00'
ws["K3"].number_format = '0.00%'

# --------------------------------------------------
# Credit Score Sheet
# --------------------------------------------------

ws_credit = wb.create_sheet("Credit Score Risk")

headers = list(credit_analysis.columns)

for col, header in enumerate(headers, 1):
    cell = ws_credit.cell(row=1, column=col, value=header)
    cell.font = Font(bold=True)

for row in credit_analysis.itertuples(index=False):
    ws_credit.append(list(row))

for row in range(2, ws_credit.max_row + 1):
    ws_credit.cell(row=row, column=4).number_format = '0.00%'

# Chart
chart = BarChart()
chart.title = "Default Rate by Credit Score"
chart.y_axis.title = "Default Rate"
chart.x_axis.title = "Credit Score Band"

data = Reference(
    ws_credit,
    min_col=4,
    min_row=1,
    max_row=ws_credit.max_row
)

cats = Reference(
    ws_credit,
    min_col=1,
    min_row=2,
    max_row=ws_credit.max_row
)

chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)

ws_credit.add_chart(chart, "F2")

# --------------------------------------------------
# DTI Sheet
# --------------------------------------------------

ws_dti = wb.create_sheet("DTI Risk")

headers = list(dti_analysis.columns)

for col, header in enumerate(headers, 1):
    cell = ws_dti.cell(row=1, column=col, value=header)
    cell.font = Font(bold=True)

for row in dti_analysis.itertuples(index=False):
    ws_dti.append(list(row))

for row in range(2, ws_dti.max_row + 1):
    ws_dti.cell(row=row, column=4).number_format = '0.00%'

# --------------------------------------------------
# Employment Sheet
# --------------------------------------------------

ws_emp = wb.create_sheet("Employment Risk")

headers = list(employment_analysis.columns)

for col, header in enumerate(headers, 1):
    cell = ws_emp.cell(row=1, column=col, value=header)
    cell.font = Font(bold=True)

for row in employment_analysis.itertuples(index=False):
    ws_emp.append(list(row))

for row in range(2, ws_emp.max_row + 1):
    ws_emp.cell(row=row, column=4).number_format = '0.00%'

# --------------------------------------------------
# Loan Purpose Sheet
# --------------------------------------------------

ws_purpose = wb.create_sheet("Loan Purpose")

headers = list(purpose_analysis.columns)

for col, header in enumerate(headers, 1):
    cell = ws_purpose.cell(row=1, column=col, value=header)
    cell.font = Font(bold=True)

for row in purpose_analysis.itertuples(index=False):
    ws_purpose.append(list(row))

for row in range(2, ws_purpose.max_row + 1):
    ws_purpose.cell(row=row, column=4).number_format = '0.00%'

# --------------------------------------------------
# Raw Data
# --------------------------------------------------

ws_raw = wb.create_sheet("Raw Data")

for col, header in enumerate(df.columns, 1):
    cell = ws_raw.cell(row=1, column=col, value=header)
    cell.font = Font(bold=True)

for row in df.itertuples(index=False):
    ws_raw.append(list(row))

# --------------------------------------------------
# Project Notes
# --------------------------------------------------

ws_notes = wb.create_sheet("Project Notes")

notes = [
    ["Project", "Loan Portfolio & Credit Risk Analysis"],
    ["Dataset", "Synthetic loan portfolio"],
    ["Loans", total_loans],
    ["Total Loan Amount", total_loan_amount],
    ["Average Loan Amount", average_loan_amount],
    ["Average Credit Score", average_credit_score],
    ["Default Rate", default_rate],
    ["Tools", "Python, SQL, Excel, Power BI"],
    ["Important", "The dataset is synthetic and does not represent real bank customers."]
]

for row in notes:
    ws_notes.append(row)

# --------------------------------------------------
# Formatting
# --------------------------------------------------

for sheet in wb.worksheets:
    for column in sheet.columns:
        max_length = 0

        for cell in column:
            if cell.value is not None:
                max_length = max(max_length, len(str(cell.value)))

        column_letter = get_column_letter(column[0].column)
        sheet.column_dimensions[column_letter].width = min(max_length + 2, 35)

# Freeze panes
for sheet in wb.worksheets:
    sheet.freeze_panes = "A2"

# --------------------------------------------------
# Save
# --------------------------------------------------

output_file = (
    "dashboard/"
    "Loan_Portfolio_Credit_Risk_Analysis.xlsx"
)

wb.save(output_file)

print("EXCEL DASHBOARD CREATED")
print("-----------------------")
print(f"File: {output_file}")
print("Sheets:")
for sheet in wb.sheetnames:
    print(f"- {sheet}")