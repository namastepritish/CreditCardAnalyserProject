"""
src/categorizer.py — V0.3

Classifies each transaction into a category + spend_type + confidence,
so the cashback engine can auto-apply rules without asking the user to
tag every single transaction manually.

confidence: "high" (known merchant/pattern match) or "low" (fallback guess).
Only "low" confidence transactions should be shown to the user for review.
"""
import re

# merchant keyword -> category
CATEGORY_KEYWORDS = {
    "Shopping":      ["amazon", "flipkart", "myntra", "ajio", "meesho"],
    "Food Delivery": ["swiggy", "zomato", "blinkit"],
    "Groceries":     ["bigbasket", "grofers", "dmart", "big bazaar", "reliance fresh"],
    "Travel":        ["irctc", "makemytrip", "goibibo", "redbus", "uber", "ola"],
    "Entertainment": ["bookmyshow", "netflix", "hotstar", "spotify"],
    "Bills/Utility":  ["electricity", "broadband", "utility", "recharge"],
    "Fuel":          ["petrol", "diesel", "fuel", "hpcl", "iocl", "bpcl"],
}

UPI_PATTERN = re.compile(r"\bupi\b", re.I)


def classify_transaction(description: str, amount: float) -> dict:
    """
    Returns: {category, spend_type, confidence}
    spend_type is "online" or "offline" — feeds directly into the
    cashback rule buckets from cards/sbi_cashback.py.
    """
    desc_lower = description.lower()

    # 1. Known online merchant -> high confidence, online
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in desc_lower for kw in keywords):
            spend_type = "offline" if category == "Fuel" else "online"
            return {"category": category, "spend_type": spend_type, "confidence": "high"}

    # 2. UPI transaction -> high confidence, offline, only if amount >= 100
    if UPI_PATTERN.search(desc_lower):
        if amount >= 100:
            return {"category": "UPI Payment", "spend_type": "offline", "confidence": "high"}
        return {"category": "UPI Payment (below threshold)", "spend_type": "offline", "confidence": "high"}

    # 3. Nothing matched -> low confidence fallback, default offline
    return {"category": "Uncategorized", "spend_type": "offline", "confidence": "low"}