from flask import Flask, render_template, jsonify, request
import psycopg2

app = Flask(__name__, template_folder='html', static_folder='assets')

# PostgreSQL database configuration
DB_HOST = 'localhost'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'admin123'


def fetch_fund_names(category):
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()

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


if __name__ == '__main__':
    app.run(debug=True)
