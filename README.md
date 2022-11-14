Warning! This repo is not in a working state. Several changes need to be made in order for this to run.

A collection of scripts which parse and aggregate the data from various different bank and credit card statement sources and upload them to a Google Sheet.

### Dependencies

- Install Python 3
- Install any remaining dependencies using pip.

### Google Sheet Integration steps:

- Go to [this google sheet](https://docs.google.com/spreadsheets/d/1EXGhg0XL_tdtYT6HBt-MImQPYWP0Sb69Angku1a95MI/edit?usp=sharing) and make a copy.
- In the `helper_google_sheets.py` file, replace the values of `_c_and_t_id` and `_all_data_id` with the GIDs of the `C&T` and `All Data` tab in your copied Google sheet.
- Go to Google Developer Console: https://console.developers.google.com
- New Project -> Activate Drive and Sheets API
- Create credentials
- service account -> name + role=editor
- create key and download json, reaname it as `finance-scripts-auth.json` and replace the existing file in this folder.

### Steps to run the script:

- Download the statements from any of the supported bank websites (each bank's individual steps are written below).
- Save these statements in the `statements` folder.
- In the `helper_parser.py` file, you need to replace the values in the `if` statements with the format of your own report files.
- Run `_main.py`. This will import all the data from the statements in the folder and merge it with the data from the [Expense tracking Google Sheet](https://docs.google.com/spreadsheets/d/1wMa1rXAPWorjkkYvv0AVNjPZqmDa41ptbUa0Qx6JoZo/edit#gid=1983578923). The script will then upload back all this data to the spreadsheet.

### Debugging:

- Instead of running the `_main.py` file, you can also run individual parsers to debug if something breaks.

### Steps to download the statement from each website:

#### HDFC Savings Account:

- Enquire
- A/c Statement - Last 5 years
- Specific period: Last month
- Excel format

#### HDFC Credit Card:

- Cards
- Credit Cards
- Enquire
- View Statement
- Last month

#### Kotak Mahindra Savings Account:

- Statements > Account Statements
- Recent Transactions > Last Month
- Download Statements > Download > CSV
- Rename add random number at end

#### ICICI Savings Account:

- View Statement
- Update transaction date / Select Transaction Period
- View Detailed Statement
- Download details as: XLS file.
