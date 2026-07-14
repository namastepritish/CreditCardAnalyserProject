"""
src/cashback_engine.py

The generic cashback calculation engine. This file knows NOTHING about
SBI or HDFC specifically — it just knows how to apply a "rules"
dictionary (in the shape defined by cards/sbi_cashback.py) to a
DataFrame of transactions. This separation is the whole point: swap in
HDFC_MILLENNIA_RULES later and this file doesn't change at all.
"""

import pandas as pd


def classify_spend_type(description: str, known_online_merchants: list) -> str:
    """
    Very simple online/offline classifier for V0.2.

    Real bank statements identify online vs offline via Merchant Category
    Code (MCC), which we don't have access to from a plain Excel/PDF
    export. So for now we do keyword matching on the merchant description.
    This is a placeholder — V0.3 will build a proper category classifier.
    """
    desc_lower = description.lower()
    for merchant in known_online_merchants:
        if merchant in desc_lower:
            return "online"
    return "offline"


def is_excluded(description: str, excluded_keywords: list) -> bool:
    """Returns True if this transaction matches an excluded category."""
    desc_lower = description.lower()
    return any(keyword in desc_lower for keyword in excluded_keywords)


def calculate_expected_cashback(transactions_df: pd.DataFrame, card_rules: dict) -> dict:
    """
    Applies `card_rules` to every Debit transaction in `transactions_df`
    and returns a summary dictionary.

    Parameters
    ----------
    transactions_df : DataFrame with at least ['Description', 'Amount', 'Type'] columns
    card_rules       : a rules dict shaped like cards.sbi_cashback.SBI_CASHBACK_RULES

    Returns
    -------
    dict with:
        expected_cashback_total : float
        bucket_breakdown        : {bucket_name: amount_earned}
        transaction_details     : list of per-transaction dicts (useful for reports later)
    """
    # Only spending transactions earn cashback — not payments, existing
    # cashback credits, or tax lines. Filter first so the loop below only
    # ever sees rows that are actually relevant.
    spend_rows = transactions_df[transactions_df["Type"] == "Debit"]

    # Track how much cashback each bucket (e.g. "Online spends") has
    # accumulated so far, so we can enforce the per-bucket cap as we go.
    bucket_totals = {bucket["name"]: 0.0 for bucket in card_rules["buckets"]}
    transaction_details = []

    for index, row in spend_rows.iterrows():
        description = row["Description"]
        amount = row["Amount"]

        if is_excluded(description, card_rules["excluded_keywords"]):
            transaction_details.append({
                "description": description, "amount": amount,
                "bucket": "Excluded", "cashback_earned": 0.0,
            })
            continue

        spend_type = classify_spend_type(description, card_rules["known_online_merchants"])

        # Find the bucket whose spend_type matches (online -> "Online spends", etc.)
        matching_bucket = next(
            (b for b in card_rules["buckets"] if b["spend_type"] == spend_type), None
        )
        if matching_bucket is None:
            transaction_details.append({
                "description": description, "amount": amount,
                "bucket": "Unmatched", "cashback_earned": 0.0,
            })
            continue

        bucket_name = matching_bucket["name"]
        raw_cashback = amount * matching_bucket["rate"]

        # Enforce the cap: don't let this bucket's total exceed its cap.
        already_earned = bucket_totals[bucket_name]
        remaining_capacity = max(0.0, matching_bucket["cap"] - already_earned) \
            if matching_bucket["cap"] is not None else raw_cashback
        actual_cashback = min(raw_cashback, remaining_capacity)

        bucket_totals[bucket_name] += actual_cashback
        transaction_details.append({
            "description": description, "amount": amount,
            "bucket": bucket_name, "cashback_earned": round(actual_cashback, 2),
        })

    expected_total = round(sum(bucket_totals.values()), 2)

    return {
        "expected_cashback_total": expected_total,
        "bucket_breakdown": {k: round(v, 2) for k, v in bucket_totals.items()},
        "transaction_details": transaction_details,
    }