"""
cards/sbi_cashback.py

Cashback rules for the SBI Cashback Credit Card, as data — not as
scattered if/else logic. Every rule is a dictionary describing:

  name        -> human-readable label (shows up in reports)
  spend_type  -> "online" or "offline" (which bucket this rule applies to)
  rate        -> cashback rate as a decimal (0.05 = 5%)
  cap         -> maximum cashback this specific bucket can earn per
                 statement cycle, in rupees (None = no cap)
  excluded_keywords -> if a transaction's description matches any of
                 these, it earns ZERO cashback even if it's online/offline

IMPORTANT: SBI revised this card's terms effective 1 April 2026 (the
online cap was cut from ~₹5,000 to ₹2,000, and new exclusions were
added). Bank T&Cs change — this file should be the ONE place you update
when that happens, which is the entire point of separating rules from
logic. Always double check against SBI's official Key Fact Statement
before relying on this for real money decisions.
"""

SBI_CASHBACK_RULES = {
    "card_name": "SBI Cashback Credit Card",
    "effective_from": "2026-04-01",
    "buckets": [
        {
            "name": "Online spends",
            "spend_type": "online",
            "rate": 0.05,
            "cap": 2000.0,
        },
        {
            "name": "Offline spends",
            "spend_type": "offline",
            "rate": 0.01,
            "cap": 2000.0,
        },
    ],
    # Categories/keywords that earn ZERO cashback regardless of online/offline.
    # Matched against the transaction description, case-insensitive.
    "excluded_keywords": [
        "fuel", "petrol", "diesel",
        "rent", "nobroker", "housing",
        "wallet", "paytm add money", "recharge wallet",
        "utility", "electricity bill", "broadband bill",
        "insurance", "lic", "premium",
        "school fee", "tuition", "education",
        "jewellery", "gift card",
        "government", "tax payment", "toll", "fastag",
        "emi",
        "gaming", "rummy", "poker",
    ],
    # Simple heuristic for classifying a transaction as online vs offline.
    # This is intentionally basic for V0.2 — real merchant-category-code
    # (MCC) based classification comes in V0.3. For now, if the merchant
    # name matches a known online platform, we call it "online"; otherwise
    # we assume "offline" (a POS swipe).
    "known_online_merchants": [
        "amazon", "flipkart", "myntra", "ajio",
        "swiggy", "zomato", "blinkit", "bigbasket",
        "bookmyshow", "irctc", "makemytrip",
        "netflix", "spotify", "hotstar",
    ],
}