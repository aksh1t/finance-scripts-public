from distutils.command.clean import clean
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from model_record import Record
from model_category import Category
from helper_validity import is_valid_amount, is_valid_date

class GSheets:

    # Reference to the spreadsheet.
    _spreadsheet = None

    # TODO: Replace these are the GIDs for the respective worksheets.
    _c_and_t_id = 123
    _all_data_id = 123

    categorization_data = {}
    all_data = set([])
    
    def __init__(self):
        # Define the scope.
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

        # Add credentials to the account.
        creds = ServiceAccountCredentials.from_json_keyfile_name('finance-scripts-auth.json', scope)

        # Authorize the client.
        client = gspread.authorize(creds)

        # Get the document instance.
        self._spreadsheet = client.open('Expense Tracking')

        # Read data into memory.
        self.read_categorization_data()
        self.read_all_data()

    def read_categorization_data(self):
        # Get the Categorization & Tagging worksheet.
        categorization_and_tagging_sheet = self._spreadsheet.get_worksheet_by_id(self._c_and_t_id)

        values = categorization_and_tagging_sheet.get_all_values()
        
        for value in values[1:]:
            d = Category(value[0], value[1], value[2])
            self.categorization_data[value[0]] = d

    def write_categorization_data(self):
        # Get the Categorization & Tagging worksheet.
        categorization_and_tagging_sheet = self._spreadsheet.get_worksheet_by_id(self._c_and_t_id)
        
        rows = []
        for key, value in self.categorization_data.items():
            rows.append(value.to_string_array())

        row_count = categorization_and_tagging_sheet.row_count
        categorization_and_tagging_sheet.delete_rows(2, row_count - 1)

        categorization_and_tagging_sheet.insert_rows(rows, 2, value_input_option="USER_ENTERED")
        
    def read_all_data(self):        
        # Get the All Data worksheet.
        all_data_sheet = self._spreadsheet.get_worksheet_by_id(self._all_data_id)

        values = all_data_sheet.get_all_values()
        
        for value in values:
            dt = value[0]
            a = value[1]
            if is_valid_date(dt) and is_valid_amount(a):
                record = Record(is_valid_date(dt, return_value=True), is_valid_amount(a, return_value=True), value[2], value[3], value[5], value[4], value[6])
                self.all_data.add(record)

    def write_all_data(self, data):
        # Get the All Data worksheet.
        all_data_sheet = self._spreadsheet.get_worksheet_by_id(self._all_data_id)
        
        rows = []
        sorted_data = sorted(list(data))
        for d in sorted_data:
            rows.append(d.to_string_array())

        row_count = all_data_sheet.row_count
        all_data_sheet.delete_rows(2, row_count - 1)

        all_data_sheet.insert_rows(rows, 2, value_input_option="USER_ENTERED")

    def update_record(self, record):
        clean_detail = record.cleaned_detail()

        if record.category_m != "":
            record.category_a = record.category_m
            exists = False
            for detail, category_object in self.categorization_data.items():
                if detail in clean_detail:
                    exists = True
                    if record.note == "":
                        record.note = category_object.note
                    break
            if exists == False:
                self.categorization_data[clean_detail] = Category(clean_detail, record.category_m, record.note)
        
        if record.category_m == "" and record.category_a != "":
            exists = False
            for detail, category_object in self.categorization_data.items():
                if detail in clean_detail:
                    exists = True
                    if record.note == "":
                        record.note = category_object.note
                    break
            if exists == False:
                self.categorization_data[clean_detail] = Category(clean_detail, record.category_a, record.note)
        
        if record.category_m == "" and record.category_a == "":
            for detail, category_object in self.categorization_data.items():
                if detail in clean_detail:
                    record.category_a = category_object.category
                    if record.note == "":
                        record.note = category_object.note
