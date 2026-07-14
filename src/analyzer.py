def analyze_transactions(data):


    total_spend = data[
        data["Type"] == "Debit"
    ]["Amount"].sum()


    total_cashback = data[
        data["Type"] == "Cashback"
    ]["Amount"].sum()


    total_payment = data[
        data["Type"] == "Payment"
    ]["Amount"].sum()


    total_tax = data[
        data["Type"] == "Tax"
    ]["Amount"].sum()


    return {
        "Total Spending": total_spend,
        "Total Cashback": total_cashback,
        "Total Payment": total_payment,
        "Total Taxes": total_tax,
        "spending": total_spend,
        "cashback": total_cashback,
        "payment": total_payment,
        "tax": total_tax,
    }