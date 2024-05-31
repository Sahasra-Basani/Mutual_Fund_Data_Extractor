from flask import Flask, render_template, jsonify, request, make_response
import psycopg2
from excel.excel_reader_All import insert_in_stock_table
import os
import json

with open("config.json") as f:
    config = json.load(f)

app = Flask(__name__, template_folder='html', static_folder='assets')

# PostgreSQL database configuration
DB_HOST = config["database"]["host"]
DB_NAME = config["database"]["database_name"]
DB_USER = config["database"]["username"]
DB_PASSWORD = config["database"]["password"]


@app.route('/upload_excel', methods=['POST'])
def upload_excel():
    # Get the file path sent from the JavaScript code
    file_path = request.json.get('file_path')

    print("file_path:", file_path)

    # Check if a file path was received
    if not file_path:
        return jsonify({'success': False, 'message': 'No file path received'})

    # Check if the file exists
    if not os.path.isfile(file_path):
        return jsonify({'success': False, 'message': 'File not found'})

    # Call the method in excel_reader_All.py to process the file
    insert_in_stock_table(file_path)

    # Return a JSON response indicating success
    return jsonify({'success': True, 'message': 'File uploaded successfully'})


def fetch_fund_names(category):
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()

    # Check the value of category
    if category == 'All' or category == 'ALL':
        # Query to fetch all the fund names
        cursor.execute("SELECT fund_name FROM mutual_fund_data.fund_details")
        fund_names = [row[0] for row in cursor.fetchall()]
    else:
        # Query to fetch fund names based on category
        cursor.execute("SELECT distinct(f1.fund_name) FROM mutual_fund_data.fund_details f1 "
                       "JOIN mutual_fund_data.stock_details s1 ON s1.fund_id = f1.id WHERE s1.category = %s", (category,))
        fund_names = [row[0] for row in cursor.fetchall()]

    print("fund_names:", fund_names)

    cursor.close()
    conn.close()

    return fund_names


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fetch_fund_names', methods=['GET'])
def fetch_fund_names_route():
    category = request.args.get('category')
    if not category:
        return jsonify([])
    fund_names = fetch_fund_names(category)
    return jsonify(fund_names)


@app.route('/compare', methods=['GET'])
def compare_funds():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()

    category = request.args.get('category')
    fund_name = request.args.get('fund_name')

    print('category app:', category)
    print('fund_name app:', fund_name)

    fund_names = "'" + "','".join(fund_name.split(',')) + "'"
    len_fund = len(fund_names.split(','))
    print('fund_names app:', fund_names)
    print('len_fund app:', len_fund)

    if category == 'All' or category == 'ALL':
        if 'All' in fund_names:
            print("Fund Name All!!!!!!!!!!!!!!!!")
            query = f"""
            SELECT sd.isin_no, 
            MAX(mon_yr) AS max_mon_yr,
            MAX(sd.stock_name) AS stock_name,
            COUNT(sd.isin_no) AS common_stocks_count,
            SUM(
                CAST(sd.amount AS NUMERIC)
            ) AS invested_amount,
            STRING_AGG(
            CASE 
                WHEN POSITION('(' IN fd.fund_name) > 0 THEN 
                    LEFT(fd.fund_name, POSITION('(' IN fd.fund_name) - 1) 
                ELSE 
                    fd.fund_name 
            END, ', '
            ) AS fund_name_list
            FROM mutual_fund_data.stock_details sd
            JOIN mutual_fund_data.fund_details fd ON sd.fund_id = fd.id
            GROUP BY sd.isin_no
            ORDER BY common_stocks_count desc;
            """
        else:
            print("Fund Name Available!!!!!!!!!!!!!!!!")
            if len_fund > 1:
                # Construct the query dynamically based on selected values
                query = f"""
                SELECT sd.isin_no, 
                MAX(mon_yr) AS max_mon_yr,
                MAX(sd.stock_name) AS stock_name,
                COUNT(sd.isin_no) AS common_stocks_count,
                SUM(
                    CAST(sd.amount AS NUMERIC)
                ) AS invested_amount,
                STRING_AGG(
                CASE 
                    WHEN POSITION('(' IN fd.fund_name) > 0 THEN 
                        LEFT(fd.fund_name, POSITION('(' IN fd.fund_name) - 1) 
                    ELSE 
                        fd.fund_name 
                END, ', '
                ) AS fund_name_list
                FROM mutual_fund_data.stock_details sd
                JOIN mutual_fund_data.fund_details fd ON sd.fund_id = fd.id
                WHERE fd.fund_name IN ({fund_names})
                GROUP BY sd.isin_no
                ORDER BY common_stocks_count desc;
                """
            else:
                query = query_fundwise_data(fund_names)
    else:
        if 'All' in fund_names:
            print("Fund Name All!!!!!!!!!!!!!!!!")
            query = f"""
            SELECT sd.isin_no, 
            MAX(mon_yr) AS max_mon_yr,
            MAX(sd.stock_name) AS stock_name,
            COUNT(sd.isin_no) AS common_stocks_count,
            SUM(
                CAST(sd.amount AS NUMERIC)
            ) AS invested_amount,
            STRING_AGG(
            CASE 
                WHEN POSITION('(' IN fd.fund_name) > 0 THEN 
                    LEFT(fd.fund_name, POSITION('(' IN fd.fund_name) - 1) 
                ELSE 
                    fd.fund_name 
            END, ', '
            ) AS fund_name_list
            FROM mutual_fund_data.stock_details sd
            JOIN mutual_fund_data.fund_details fd ON sd.fund_id = fd.id
            WHERE sd.category = '{category}'
            GROUP BY sd.isin_no
            ORDER BY common_stocks_count desc;
            """
        else:
            if len_fund > 1:
                # Construct the query dynamically based on selected values
                query = f"""
                SELECT sd.isin_no, 
                MAX(mon_yr) AS max_mon_yr,
                MAX(sd.stock_name) AS stock_name,
                COUNT(sd.isin_no) AS common_stocks_count,
                SUM(
                    CAST(sd.amount AS NUMERIC)
                ) AS invested_amount,
                STRING_AGG(
                CASE 
                    WHEN POSITION('(' IN fd.fund_name) > 0 THEN 
                        LEFT(fd.fund_name, POSITION('(' IN fd.fund_name) - 1) 
                    ELSE 
                        fd.fund_name 
                END, ', '
                ) AS fund_name_list
                FROM mutual_fund_data.stock_details sd
                JOIN mutual_fund_data.fund_details fd ON sd.fund_id = fd.id
                WHERE fd.fund_name IN ({fund_names})
                AND sd.category = '{category}'
                GROUP BY sd.isin_no
                ORDER BY common_stocks_count desc;
                """
            else:
                query = query_fundwise_data(fund_names)

    # Execute the query
    cursor.execute(query)

    print("query:", query)

    comparison_results = cursor.fetchall()

    # Convert results to JSON and return
    return jsonify(comparison_results)


def query_fundwise_data(fund_names):
    if fund_names:
        query = f"""
        SELECT sd.isin_no, sd.mon_yr, sd.stock_name, sd.quantity, sd.amount, sd.holding_share, 
        CASE 
            WHEN POSITION('(' IN fd.fund_name) > 0 THEN 
                LEFT(fd.fund_name, POSITION('(' IN fd.fund_name) - 1) 
            ELSE 
                fd.fund_name 
        END AS fund_name 
        FROM mutual_fund_data.stock_details sd
        JOIN mutual_fund_data.fund_details fd ON sd.fund_id = fd.id
        WHERE fd.fund_name = {fund_names}
        ORDER BY sd.holding_share desc;
        """
        return query


if __name__ == '__main__':
    app.run(debug=True)
