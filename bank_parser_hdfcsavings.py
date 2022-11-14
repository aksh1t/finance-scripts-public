from helper_validity import is_valid_date, is_valid_amount
from model_record import Record
import xlrd

class HDFCSavingsParser:

    def __init__(self, filename):
        print("Parsing HDFC Savings Account Statement: " + filename)
        self.filename = filename
        self.owner = ""
        f = filename.split("/")[-1]
        self.owner = "Name"

    def parse(self):
        data = set([])
        wb = xlrd.open_workbook(self.filename)
        sheet = wb.sheet_by_index(0)
        
        for x in range(0, sheet.nrows):
            dt = sheet.cell_value(x, 0)
            c = ""
            a_cr = sheet.cell_value(x, 5)
            a_db = sheet.cell_value(x, 4)
            d = sheet.cell_value(x, 1)
            if type(dt) == str and is_valid_date(dt) and (type(a_cr) == float or type(a_db) == float):
                a = a_cr if type(a_cr) == float else a_db * -1
                record = Record(is_valid_date(dt, return_value=True), a, c, "", d, "HDFC Savings (" + self.owner + ")", "")
                data.add(record)
                
        return data

# Driver code for testing:

# parser = HDFCSavingsParser("statements/53975105_1617341524245.xls")
# parser.parse()