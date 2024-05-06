import os.path
import xlrd
from database.database import connect_to_db
import process_date
import json

with open("config.json") as f:
    config = json.load(f)

# Get current date and time
current_date = process_date.current_date

# Get the previous month
prev_mon_name_MM = process_date.prev_mon_name_MM

# Get the current year YYYY
current_year_yyyy = process_date.current_year_yyyy
current_year_yy = process_date.current_year_yy


def insert_in_stock_table():
    category = ""
    fund_id = 0
    cell_val_6 = 0.00

    try:
        # Input File path
        # file_path = "F:/Python Projects/Funds details/Nippon/NIMF-MONTHLY-PORTFOLIO-REPORT-March-24.xls"
        file_name = config["other_settings"]["excel_path_nippon"]
        file_path = file_name+f"{prev_mon_name_MM}-{current_year_yy}.xls"
        print("file_path", file_path)

        if not os.path.exists(file_path):
            print("File not found!")
            exit()
        else:
            mon_yr = prev_mon_name_MM+'_'+str(current_year_yyyy)

            # Open the Excel file
            workbook = xlrd.open_workbook(file_path)

            # Sheets to be read from excel
            sheet_names = ['SC', 'GF', 'EA', 'TS']

            for sheet_name in sheet_names:
                # Select a worksheet
                worksheet = workbook.sheet_by_name(sheet_name)

                # Insert data in the fund_details table
                insert_in_fund_table(worksheet)

                if sheet_name == 'SC':
                    category = "Small Cap"
                elif sheet_name == 'GF':
                    category = "Mid Cap"
                elif sheet_name == 'EA':
                    category = "Large Cap"
                elif sheet_name == 'TS':
                    category = "Tax Saver"

                # Define the list of column indices you want to read
                columns_to_read = [1, 2, 3, 4, 5, 6]  # Columns 2, 3, 4, 5, 6 and 7 (0-indexed)

                # Define the starting row 7
                start_row = 6  # Row 7 (0-indexed)

                # Loop through rows starting from the 7th row
                for row_idx in range(start_row, worksheet.nrows):

                    row_val = worksheet.cell_value(row_idx, 1)
                    row_val6 = worksheet.cell_value(row_idx, 6)

                    # Check if the value in column 2 and column 7 is not null
                    if row_val and row_val6:

                        # Get fund_id from fund_details table
                        fund_id = get_fund_id(category)

                        for col_idx in columns_to_read:
                            cell_value_6 = str(worksheet.cell_value(row_idx, 6)).replace('$', '').replace('%', '')
                            cell_val_6 = round(float(cell_value_6) * 100, 2)

                        try:
                            # Insert data into the database in stock_details table
                            cursor.execute('''INSERT INTO mutual_fund_data.stock_details(fund_id, created_date, 
                            mon_yr, category, isin_no, stock_name, industry, quantity, amount, holding_share) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                                           (fund_id,
                                            current_date,
                                            mon_yr,
                                            category,
                                            worksheet.cell_value(row_idx, 1),
                                            worksheet.cell_value(row_idx, 2),
                                            worksheet.cell_value(row_idx, 3),
                                            worksheet.cell_value(row_idx, 4),
                                            worksheet.cell_value(row_idx, 5),
                                            cell_val_6))

                        except Exception as e:
                            print("Issue occurred inserting data into database in stock_details table!!!", str(e))

                print("Data inserted successfully in the stock_details table for {} Sheet!!!".format(sheet_name))

    except Exception as e:
        print("Issue while working on reading excel", str(e))


def insert_in_fund_table(worksheet):
    try:
        # fund_house and created_date values
        fund_house = "Nippon India Mutual Fund"

        # Insert the data into the database in fund_details table
        cursor.execute('''INSERT INTO mutual_fund_data.fund_details(created_date, fund_name, fund_house) 
        VALUES (%s, %s, %s)''',
                       (current_date,
                        worksheet.cell_value(0, 1),
                        fund_house))
        print("Data inserted successfully in the fund_details table!!!")

    except Exception as e:
        print("Issue occurred inserting dta into database in fund_details table!!!", str(e))


def get_fund_id(category):
    try:
        # Get fund_id from fund_details table
        query = ("SELECT id FROM mutual_fund_data.fund_details WHERE fund_house = 'Nippon India Mutual Fund' "
                 "and lower(fund_name) LIKE %s LIMIT 1")
        cursor.execute(query, ('%' + category.lower() + '%',))
        res = cursor.fetchone()
        return res

    except Exception as e:
        print("Issue occurred while getting the fund_id from the fund_details table!!!", str(e))


# Database connection details
host = config["database"]["host"]
port = config["database"]["port"]
dbname = config["database"]["database_name"]
user = config["database"]["username"]
password = config["database"]["password"]

try:
    # Connect to the PostgreSQL database
    connection = connect_to_db(dbname, user, password, host, port)

    if connection:
        cursor = connection.cursor()
        print("**************Connection Successful*******************")

        insert_in_stock_table()

except Exception as e:
    print("Issue occurred while connecting to the database", str(e))

finally:
    # Commit changes and close the connection
    connection.commit()
    connection.close()



