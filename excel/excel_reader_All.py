import os.path
import xlrd
import os
from database.database import connect_to_db
from process_date import DateDetails as Dd
import json

with open("config.json") as f:
    config = json.load(f)


def insert_in_stock_table(file_n):

    # Get current date and time
    current_date = Dd.current_date

    # Get the previous month
    prev_mon_name_mm = Dd.prev_mon_name_MM

    # Get the current year YYYY
    current_year_yyyy = Dd.current_year_yyyy

    category = ""
    fund_id = 0
    cell_val_5 = 0.00
    print("file_n:", file_n)
    try:
        # Input File path
        # file_name = config["other_settings"]["excel_path_all"]
        # file_path = file_name+f"{prev_mon_name_MM}-{current_year_yy}.xls"

        # excel_files = glob.glob(os.path.join(file_name, '*.xls'))
        # file_path = excel_files[0]

        filename = os.path.basename(file_n)
        print("File Name!:", filename)

        if not os.path.exists(file_n):
            print("File not found!")
            exit()
        else:
            mon_yr = prev_mon_name_mm+'_'+str(current_year_yyyy)

            # Open the Excel file
            workbook = xlrd.open_workbook(file_n)

            # Sheets to be read from excel
            sheet_names = workbook.sheet_names()
            print(sheet_names)

            for sheet_name in sheet_names:
                # Select a worksheet
                worksheet = workbook.sheet_by_name(sheet_name)

                # Get fund_id from fund_details table
                fund_id = get_fund_id(sheet_name, filename)

                if 'Small' in sheet_name:
                    category = "Small Cap"
                elif 'Mid' in sheet_name:
                    category = "Mid Cap"
                elif 'Large' in sheet_name:
                    category = "Large Cap"
                elif 'Tax' in sheet_name:
                    category = "Tax Saver"
                else:
                    category = "Others"

                    # Define the list of column indices you want to read
                columns_to_read = [0, 1, 2, 3, 4, 5]  # Columns 1, 2, 3, 4, 5 and 6 (0-indexed)

                # Define the starting row 2
                start_row = 1  # Row 2 (0-indexed)

                print("fund_id:", fund_id)

                if fund_id:
                    print("fund_id Available")

                    # Update flag in the stock_details table if fund_id is available
                    update_flag_stocks(fund_id)

                    conn = db_connection()
                    cursor = conn.cursor()

                    # Loop through rows starting from the 2nd row
                    for row_idx in range(start_row, worksheet.nrows):

                        row_val = worksheet.cell_value(row_idx, 0)
                        row_val5 = worksheet.cell_value(row_idx, 5)

                        # Check if the value in column 1 and column 6 is not null
                        if row_val and row_val5:

                            for col_idx in columns_to_read:
                                cell_value_5 = str(worksheet.cell_value(row_idx, 5)).replace('$', '').replace('%', '')
                                cell_val_5 = round(float(cell_value_5) * 100, 2)

                            try:
                                # Insert data into the database in stock_details table
                                cursor.execute('''INSERT INTO mutual_fund_data.stock_details(fund_id, created_date, 
                                        mon_yr, category, isin_no, stock_name, industry, quantity, amount, 
                                        holding_share, is_current_mon) 
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                                               (fund_id, current_date, mon_yr, category,
                                                worksheet.cell_value(row_idx, 0),
                                                worksheet.cell_value(row_idx, 1),
                                                worksheet.cell_value(row_idx, 2),
                                                worksheet.cell_value(row_idx, 3),
                                                worksheet.cell_value(row_idx, 4),
                                                cell_val_5, "Y"))

                            except Exception as e:
                                print("Issue occurred inserting data into database in stock_details table!!!", str(e))

                    conn.commit()
                    conn.close()

                    print("Data inserted successfully in the stock_details table for {} Sheet!!!".format(sheet_name))

                else:
                    print("fund_id not Available")

                    # Insert data in the fund_details table
                    insert_in_fund_table(current_date, sheet_name, filename)

                    # Get fund_id from fund_details table
                    fund_id = get_fund_id(sheet_name, filename)

                    conn = db_connection()
                    cursor = conn.cursor()

                    # Loop through rows starting from the 2nd row
                    for row_idx in range(start_row, worksheet.nrows):

                        row_val = worksheet.cell_value(row_idx, 0)
                        row_val5 = worksheet.cell_value(row_idx, 5)

                        # Check if the value in column 1 and column 6 is not null
                        if row_val and row_val5:

                            for col_idx in columns_to_read:
                                cell_value_5 = str(worksheet.cell_value(row_idx, 5)).replace('$', '').replace('%', '')
                                cell_val_5 = round(float(cell_value_5) * 100, 2)

                            try:
                                # Insert data into the database in stock_details table
                                cursor.execute('''INSERT INTO mutual_fund_data.stock_details(fund_id, created_date, 
                                        mon_yr, category, isin_no, stock_name, industry, quantity, amount, 
                                        holding_share, is_current_mon) 
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                                               (fund_id, current_date, mon_yr, category,
                                                worksheet.cell_value(row_idx, 0),
                                                worksheet.cell_value(row_idx, 1),
                                                worksheet.cell_value(row_idx, 2),
                                                worksheet.cell_value(row_idx, 3),
                                                worksheet.cell_value(row_idx, 4),
                                                cell_val_5, "Y"))

                            except Exception as e:
                                print("Issue occurred inserting data into database in stock_details table!!!", str(e))

                    conn.commit()
                    conn.close()

                    print("Data inserted successfully in the stock_details table for {} Sheet!!!".format(sheet_name))

    except Exception as e:
        print("Issue while working on reading excel!!!! ", str(e))


def insert_in_fund_table(current_date, sheet_name, filename):
    conn = db_connection()
    cursor = conn.cursor()

    try:
        # fund_house value
        house_name = filename.split('-')[0]
        fund_house = house_name+" Mutual Fund"

        # Insert the data into the database in fund_details table
        cursor.execute('''INSERT INTO mutual_fund_data.fund_details(created_date, fund_name, fund_house) 
        VALUES (%s, %s, %s)''',
                       (current_date,
                        sheet_name,
                        fund_house))
        print("Data inserted successfully in the fund_details table!!!")

    except Exception as e:
        print("Issue occurred inserting dta into database in fund_details table!!!", str(e))

    finally:
        conn.commit()
        conn.close()


def get_fund_id(fund_name, filename):
    conn = db_connection()
    cursor = conn.cursor()

    try:
        # fund_house value
        house_name = filename.split('-')[0]
        fund_house = house_name + " Mutual Fund"

        print("fund_house:", fund_house)
        print("fund_name:", fund_name)

        # Get fund_id from fund_details table
        # query = ("SELECT id FROM mutual_fund_data.fund_details WHERE fund_house = %s "
        #          "and lower(fund_name) LIKE %s LIMIT 1")
        query = ("SELECT id FROM mutual_fund_data.fund_details WHERE fund_house = %s "
                 "and lower(fund_name) = %s LIMIT 1")
        cursor.execute(query, (fund_house, fund_name.lower()))
        res = cursor.fetchone()
        return res

    except Exception as e:
        print("Issue occurred while getting the fund_id from the fund_details table!!!", str(e))

    finally:
        conn.commit()
        conn.close()


def update_flag_stocks(fund_id):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        print("fund_id:", fund_id)

        query = ("UPDATE mutual_fund_data.stock_details SET is_current_mon = 'N' "
                 "WHERE fund_id = %s AND is_current_mon = 'Y'")
        cursor.execute(query, fund_id)
        res = cursor.fetchone()
        return res

    except Exception as e:
        print("Issue occurred while updating the flag for month in stock_details table!!!", str(e))

    finally:
        conn.commit()
        conn.close()


def db_connection():
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
            # cursor = connection.cursor()
            # print("**************Connection Successful*******************")

            return connection

    except Exception as e:
        print("Issue occurred while connecting to the database", str(e))
        return False

    # finally:
    #     # Commit changes and close the connection
    #     connection.commit()
    #     connection.close()



