from helper_validity import is_valid_date, is_valid_amount
from tabula import read_pdf
from model_record import Record

class KotakCCParser:

    # TODO: Add more strings here according to your details.
    REJECTED_STRINGS = [
        "Minimum Amount Due",
        "Total Amount Due",
        "Remember to Pay By",
        "Total Outstanding",
        "Customer Relationship Number",
        "BT, EMI & Loans",
        "Purchases &",
        "Opening Balance",
        "Amount Due",
        "Other Charges",
        "Earned this month",
        "Redeemed this month",
        "Total Credit Limit (incl. cash):",
        "Total Cash Limit:",
        "Expired this month",
        "Self Set Credit Limit:",
        "Available Cash Limit:",
        "Closing Balance",
        "Available Credit Limit:",
        "Excess payment will be adjusted against any outstanding BT",
        "Date Transaction",
        "Spends Area",
        "Amount (Rs.)",
        "Payments and Other Credits",
        "Primary Card Transactions",
        "Retail Purchases and Cash Transactions",
        "no. on the reverse of the cheque.",
        "You may drop the cheques at any Kotak ATM /Branch.",
        "What you must know!",
        "The drop box closest to you is",
        "You can contact us at",
        "Total Purchase & Other Charges",
        "*SMS EMI to 5676788 to convert your transactions into EMI or visit www.kotak.com to convert online",
        "Payment of only Minimum Dues month on month shall lead to repayment extending to a longer tenure with consequent Interest Charges (as applicable) accrued on",
        "your outstanding balances.",
        "ONLINE FUNDS TRANSFER",
    ]

    def __init__(self, filename):
        print("Parsing Kotak Credit Card Account Statement: " + filename)
        self.filename = filename

    def parse(self):
        data = []
        tables = read_pdf(self.filename, multiple_tables=True, pages='all')
        for table in tables:
            for row in table.iterrows():
                if self.is_valid_record(row[1]) and self.parse_row(row[1]) is not None:
                    data.append(self.parse_row(row[1]))
        return data

    def is_valid_record(self, items):
        filtered = filter(lambda x: type(x) == str, items)
        for item in filtered:
            for rejected in self.REJECTED_STRINGS:
                if rejected in item:
                    return False
        return True

    def parse_row(self, items):
        filtered = list(filter(lambda x: type(x) == str, items))
        if len(filtered) >= 2:
            dt = filtered[0].split(" ")[0]
            a = filtered[-1].replace(",","")
            multiplier = -1
            if " Cr" in a:
                a = a.replace(" Cr", "")
                multiplier = 1
            c = filtered[-2] if len(filtered) > 2 else ""
            d = " ".join(filtered[0].split(" ")[1:])
            if is_valid_date(dt) and is_valid_amount(a):
                return Record(is_valid_date(dt, return_value=True), is_valid_amount(a, return_value=True) * multiplier, c, "", d, "Kotak Credit Card", "")

# Driver code for testing:

# parser = KotakCCParser("statements/XXXXX682_Nov-20.pdf") # Match the number of entries manually
# data = parser.parse()
# for record in data:
#     print(record)