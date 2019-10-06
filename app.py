from flask import Flask, render_template, request, url_for, redirect, jsonify
import pandas as pd
import numpy as np
import json
import webbrowser
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

assets_colname = ["Fund Code", "Fund Name", "Asset Code", "Asset Name", "IssuerId", "Shares Outstanding", "SOD Position", "Transactions", "EOD Position", "EOD Percentage of Holdings"]
issuers_colname = ["IssuerId", "SOD Position", "Transactions", "EOD Position"]
transactions_colname = ["Fund Code", "Fund Name", "Asset Code", "Asset Name", "IssuerId", "Transactions"]

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/issuers')
def issuers():
    return render_template("issuers.html", issuers_colname = issuers_colname)

@app.route('/assets')
def assets():
    return render_template("assets.html", assets_colname = assets_colname)

@app.route('/transactions')
def transactions():
    return render_template("transactions.html", transactions_colname = transactions_colname)

@app.route('/reconcile', methods=['POST'])
def reconcile():
    input_date = request.form['input_date']
    df = pd.read_csv('raw_data/data.csv')
    df['SOD Position'] = np.random.randint(10000, 900000, df.shape[0])
    df['Transactions'] = np.random.randint(-9000, 90000, df.shape[0])
    df['EOD Position'] = df['SOD Position'] + df['Transactions']
    df['EOD Percentage of Holdings'] = df['EOD Position']/df['Shares Outstanding']
    df['EOD Percentage of Holdings'] = df['EOD Percentage of Holdings'].map('{:,.2%}'.format)
    df.to_csv(f'data/data_{input_date}.csv', index=False)
    error = 0
    return jsonify({'error': error, 'date': input_date})

@app.route('/get_issuers_table', methods=['POST'])
def get_issuers_table():
    input_date = request.form['input_date']
    try:
        df = pd.read_csv(f"data/data_{input_date}.csv")
        df_issuers = df.groupby("IssuerId", as_index = False)[["SOD Position", "Transactions", "EOD Position"]].sum()
        df_json_string = df_issuers.to_json(orient="values")
        # Convert string to json object
        df_json = json.loads(df_json_string)
        return jsonify({'date': input_date,'df': df_json})
     # If file cannot be found
    except FileNotFoundError:
        error = 1
        return jsonify({'date': input_date, 'error': error})

@app.route('/get_assets_table', methods=['POST'])
def get_assets_table():
    input_date = request.form['input_date']
    try:
        df = pd.read_csv(f"data/data_{input_date}.csv")
        df_json_string = df.to_json(orient="values")
        # Convert string to json object
        df_json = json.loads(df_json_string)
        return jsonify({'date': input_date,'df': df_json})
     # If file cannot be found
    except FileNotFoundError:
        error = 1
        return jsonify({'date': input_date, 'error': error})

@app.route('/get_transactions_table', methods=['POST'])
def get_transactions_table():
    input_date = request.form['input_date']
    try:
        df = pd.read_csv(f"data/data_{input_date}.csv")
        df_transactions = df[transactions_colname]
        df_json_string = df_transactions.to_json(orient="values")
        # Convert string to json object
        df_json = json.loads(df_json_string)
        return jsonify({'date': input_date,'df': df_json})
     # If file cannot be found
    except FileNotFoundError:
        error = 1
        return jsonify({'date': input_date, 'error': error})

@app.route('/reset', methods=['POST'])
def reset():
    mydir = "data/"
    filelist = [f for f in os.listdir(mydir) if f.endswith(".csv")]
    for f in filelist:
        print("%s is deleted" % f)
        os.remove(os.path.join(mydir, f))
    return jsonify({'error': 0})

@app.route('/submit_query', methods=['POST'])
def submit_query():
    query = request.form['query']
    df_qn = pd.read_csv("data/queries/queries.csv")
    df_add = pd.DataFrame({'Questions': [query]})
    df_qn = df_qn.append(df_add, ignore_index=True)
    df_qn.to_csv("data/queries/queries.csv", index = False)
    return jsonify({'error': 0})

@app.route('/queries')
def queries():
    df_qn = pd.read_csv("data/queries/queries.csv")
    return render_template("queries.html", df = df_qn.to_html())

# For running the App
host = "127.0.0.1"
port = "5000"
app_url = f"http://{host}:{port}/"

if __name__ == "__main__":
    # webbrowser.open(app_url)
    app.run(host = host, port = port, debug=True)


