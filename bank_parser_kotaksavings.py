from helper_validity import is_valid_date, is_valid_amount
from model_record import Record
import csv

class KotakSavingsParserOld:

    def __init__(self, filename):
        print("Parsing Old Kotak Savings Account Statement: " + filename)
        self.filename = filename

    def parse(self):
        data = set([])

        # initializing the titles and rows list
        rows = []
        
        # reading csv file
        with open(self.filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                rows.append(row)
                
        for row in rows:
            dt = row[1]
            multiplier = 1 if row[5] == "CR" else -1
            c = ""
            a = row[4]
            d = row[2].replace("\"","").replace("=","")
            if is_valid_date(dt) and is_valid_amount(a):
                record = Record(is_valid_date(dt, return_value=True), is_valid_amount(a, return_value=True) * multiplier, c, "", d, "Kotak Savings", "")
                data.add(record)
                
        return data

class KotakSavingsParserNew:

    def __init__(self, filename):
        print("Parsing New Kotak Savings Account Statement: " + filename)
        self.filename = filename

    def parse(self):
        data = set([])

        # initializing the titles and rows list
        rows = []
        
        # reading csv file
        with open(self.filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if len(row) == 9:
                    rows.append(row) 
                
        for row in rows[1:]:
            dt = row[2]
            multiplier = 1 if row[6] == "CR" else -1
            c = ""
            a = row[5]
            d = row[3].replace("\"","").replace("=","")
            if is_valid_date(dt) and is_valid_amount(a):
                record = Record(is_valid_date(dt, return_value=True), is_valid_amount(a, return_value=True) * multiplier, c, "", d, "Kotak Savings", "")
                data.add(record)

        return data

# Driver code for testing:

# parser = KotakSavingsParserOld("statements/Report-20210403182321.csv")
# parser.parse()
# data = parser.parse()