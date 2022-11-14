from helper_parser import Parser
from helper_google_sheets import GSheets

# Setup.
gs = GSheets()

# Parse bank reports from the ./statements folder.
p = Parser("statements")

# Merge the data which exists on the Google sheet with the recently parsed data.
data = gs.all_data.union(p.data)

# Update the parsed records and categorization data.
for record in data:
    gs.update_record(record)

# Write all the data back to the Google sheet.
gs.write_all_data(data)

# Write the categorization data back to the Google sheet.
gs.write_categorization_data()
