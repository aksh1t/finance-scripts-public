from helper_validity import is_valid_date, is_valid_amount
from tabula import read_pdf
from model_record import Record

class HDFCCCParser:

    # Add any rejected strings while parsing here.
    REJECTED_STRINGS = [
        "NETBANKING TRANSFER",
    ]

    def __init__(self, filename):
        print("Parsing HDFC Credit Card Statement: " + filename)
        self.filename = filename

    def parse(self):
        data = set([])
        tables = read_pdf(self.filename, multiple_tables=True, pages='all')
        for table in tables:
            for row in table.iterrows():
                if self.is_valid_record(row[1]) and self.parse_row(row[1]) is not None:
                    data.add(self.parse_row(row[1]))
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
        if len(filtered) > 2:
            dt = filtered[0].split(" ")[0]
            a = filtered[-1].replace(",","")
            multiplier = -1
            if " Cr" in a:
                a = a.replace(" Cr", "")
                multiplier = 1
            c = ""
            d = filtered[1]
            if is_valid_date(dt) and is_valid_amount(a):
                return Record(is_valid_date(dt, return_value=True), is_valid_amount(a, return_value=True) * multiplier, c, "", d, "HDFC Credit Card", "")

# Driver code for testing:

# parser = HDFCCCParser("statements/numbers_numbers_numbers.PDF")
# data = parser.parse()
# for record in data:
#     print(record)