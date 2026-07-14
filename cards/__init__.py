"""
cards/__init__.py

This file's presence is what turns the `cards/` folder into a Python
*package* — without it, `from cards.sbi_cashback import SBI_CASHBACK_RULES`
wouldn't work in some Python setups.

We're keeping it mostly empty for now (that's normal — plenty of real
__init__.py files are close to empty, they just mark the boundary of a
package). As the project grows, this is also the place where you could
expose a clean "public API" for the package, e.g.:

    from cards.sbi_cashback import SBI_CASHBACK_RULES
    from cards.hdfc_millennia import HDFC_MILLENNIA_RULES

    ALL_CARDS = {
        "SBI Cashback": SBI_CASHBACK_RULES,
        "HDFC Millennia": HDFC_MILLENNIA_RULES,
    }

so other files can do `from cards import ALL_CARDS` instead of knowing
the internal file names. We'll add that once there's a second card.
"""