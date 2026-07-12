from src.reader import read_statement
from src.analyzer import analyze_transactions


statement = read_statement(
    "data/sample_statement.xlsx"
)


summary = analyze_transactions(statement)


print("\n===== CREDIT CARD SUMMARY =====")

print(
    "Total Spending:",
    summary["spending"]
)

print(
    "Total Cashback:",
    summary["cashback"]
)

print(
    "Total Payment:",
    summary["payment"]
)

print(
    "Total Taxes:",
    summary["tax"]
)

print("==============================")