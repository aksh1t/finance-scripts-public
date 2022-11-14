import re

class Record:    
    def __init__(self, date, amount, category_m, category_a, detail, account, note):
        self.date = date # Date of the transaction.
        self.amount = amount # Amount of the transaction (+ve for credits, -ve for debits).
        self.category_m = category_m # Manually added category.
        self.category_a = category_a # Automatically classified category.
        self.detail = detail # Raw detail from the transaction.
        self.account = account # Bank account with owner name.
        self.note = note # Manually added note.

    def to_string(self):
        return "| Date: " + str(self.date.date()) + " | Amount: " + str(self.amount) + " | Category (Manual): " + self.category_m + " | Category (Automated): " + self.category_a + " | Account: " + self.account + " | Detail: " + self.detail + " | Note: " + self.note + " |"

    # Convert to an array of strings. To be used when exporting.
    def to_string_array(self):
        return [self.date.strftime("%d %b %Y"), str(self.amount), self.category_m, self.category_a, self.account, self.detail, self.note]

    # Remove all non alpha characters, put one space in between and convert to lowercase.
    def cleaned_detail(self):
        return re.sub(' +', ' ', re.compile('[^a-zA-Z]').sub(' ', self.detail)).lower()

    def __repr__(self):
        return self.to_string()
    
    def __str__(self):
        return self.to_string()

    def __eq__(self, obj):
        return self.date == obj.date and self.amount == obj.amount and self.detail == obj.detail and self.account == obj.account

    def __lt__(self, obj):
        return self.date < obj.date

    def __le__(self, obj):
        return self.date <= obj.date

    def __gt__(self, obj):
        return self.date > obj.date

    def __ge__(self, obj):
        return self.date >= obj.date

    def __hash__(self):
        return hash((self.date, self.amount, self.detail, self.account))