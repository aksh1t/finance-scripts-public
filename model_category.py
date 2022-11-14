class Category:
    
    def __init__(self, detail, category, note):
        self.detail = detail # The string to match in the detail to categorize a Record.
        self.category = category
        self.note = note

    def to_string(self):
        return "| Detail: " + self.detail + " | Category: " + self.category + " | Note: " + self.note + " |"

    # Convert to an array of strings. To be used when exporting.
    def to_string_array(self):
        return [self.detail, self.category, self.note]

    def __repr__(self):
        return self.to_string()
    
    def __str__(self):
        return self.to_string()

    def __eq__(self, obj):
        return self.detail == obj.detail and self.category == obj.category and self.note == obj.note

    def __lt__(self, obj):
        return self.category < obj.category

    def __le__(self, obj):
        return self.category <= obj.category

    def __gt__(self, obj):
        return self.category > obj.category

    def __ge__(self, obj):
        return self.category >= obj.category

    def __hash__(self):
        return hash((self.detail, self.category, self.note))