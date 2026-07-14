import unittest

import pandas as pd

from src.analyzer import analyze_transactions


class AnalyzerTests(unittest.TestCase):
    def test_summary_contains_display_keys(self):
        data = pd.DataFrame(
            [
                {"Type": "Debit", "Amount": 100.0},
                {"Type": "Cashback", "Amount": 5.0},
                {"Type": "Payment", "Amount": 20.0},
                {"Type": "Tax", "Amount": 3.0},
            ]
        )

        summary = analyze_transactions(data)

        self.assertEqual(summary["Total Spending"], 100.0)
        self.assertEqual(summary["Total Cashback"], 5.0)
        self.assertEqual(summary["Total Payment"], 20.0)
        self.assertEqual(summary["Total Taxes"], 3.0)


if __name__ == "__main__":
    unittest.main()
