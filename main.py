"""
main.py — V0.2

Workflow:
    Excel -> Reader -> Analyzer -> Cashback Engine -> Comparison -> Terminal Summary

New in V0.2: after computing the actual totals (from analyzer.py), we
now also calculate what cashback SHOULD have been earned (using the
SBI rules engine) and compare it against what the bank actually
credited. This comparison is the core value of the whole project —
everything else is supporting infrastructure for this one number.
"""

from src.reader import read_statement
from src.analyzer import analyze_transactions
from src.cashback_engine import calculate_expected_cashback
from cards.sbi_cashback import SBI_CASHBACK_RULES


def main():
    file_path = "data/sample_statement.xlsx"
    transactions_df = read_statement(file_path)

    summary = analyze_transactions(transactions_df)

    cashback_result = calculate_expected_cashback(transactions_df, SBI_CASHBACK_RULES)
    expected_cashback = cashback_result["expected_cashback_total"]
    actual_cashback = summary["cashback"]
    difference = round(expected_cashback - actual_cashback, 2)

    print("===== CREDIT CARD SUMMARY =====")
    print(f"Total Spending: {summary['spending']}")
    print(f"Total Payment: {summary['payment']}")
    print(f"Total Taxes: {summary['tax']}")
    print("--------------------------------")
    print(f"Actual Cashback (from statement): {actual_cashback}")
    print(f"Expected Cashback (calculated):   {expected_cashback}")
    print(f"Difference:                        {difference}")
    print("--------------------------------")
    print("Bucket breakdown:")
    print("\nTransaction details:")
    for t in cashback_result["transaction_details"]:
        print(f"  {t['description']:<25} ₹{t['amount']:<8} {t['bucket']:<15} +₹{t['cashback_earned']}")



    for bucket_name, amount in cashback_result["bucket_breakdown"].items():
        print(f"  {bucket_name}: {amount}")
    print("================================")

    if difference > 0:
        print(f"\n⚠️  You may be owed ₹{difference} more cashback than what was credited.")
    elif difference < 0:
        print(f"\nℹ️  Bank credited ₹{abs(difference)} more than our estimate — "
              f"check for a promotional offer our rules don't know about.")
    else:
        print("\n✅ Actual cashback matches expected cashback.")


if __name__ == "__main__":
    main()