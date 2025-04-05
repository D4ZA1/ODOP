import datetime
import glob
import json
import os
import sys

import pandas as pd
from flask import Flask, jsonify, redirect, render_template, request, url_for

# Fix path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ml_service import (get_future_price_predictions,
                        get_model_evaluation_results)

from blockchain.product import Product
from blockchain.product_blockchain import ProductBlockchain
from blockchain.transaction import Transaction
from blockchain.transaction_blockchain import TransactionBlockchain
from security.key_generation import generate_keys

app = Flask(__name__)





# Key pair
private_key, public_key = generate_keys()

# Blockchain instances
blockchain = TransactionBlockchain()
product_blockchain = ProductBlockchain()

# Load saved chains if they exist
blockchain.load_chain("data/transaction_chain.json")
product_blockchain.load_chain("data/product_chain.json")

IMPORTED_LOG = "imported_files.json"

def load_imported_files():
    if os.path.exists(IMPORTED_LOG):
        with open(IMPORTED_LOG, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_imported_file(file_name):
    imported = load_imported_files()
    imported.append(file_name)
    with open(IMPORTED_LOG, "w") as f:
        json.dump(imported, f)

def import_excel_data_on_startup(folder_path="dataset"):
    try:
        imported_files = load_imported_files()
        if imported_files:
            print("[INFO] Skipping import — log file already has entries.")
            return

        csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
        if not csv_files:
            print("[INFO] No CSV files found in the folder.")
            return

        print(f"[INFO] Found {len(csv_files)} CSV file(s) in '{folder_path}'.")
        print(f"[INFO] Importing only first 2 files: {[os.path.basename(f) for f in csv_files[:2]]}")
        for file in csv_files[0:1]:
            file_name = os.path.basename(file)
            if file_name in imported_files:
                print(f"[SKIPPED] {file_name} already imported.")
                continue

            try:
                df = pd.read_csv(file)
                print(f"[INFO] Processing {file_name}")
                product_id = str(df.iloc[0]["Commodity_Code"])
                name = str(df.iloc[0]["Commodity"])
                origin_district = str(df.iloc[0]["District"])
                markets = df["Market"].unique()
                print(f"  [INFO] Found markets: {markets}")
                for market in markets:
                    market_rows = df[df["Market"] == market]
                    product_data = {
                        "product_id": product_id,
                        "name": name,
                        "origin_district": origin_district,
                        "market": market,
                        "timestamp": str(market_rows.iloc[0]["Arrival_Date"])
                    }
                    product_blockchain.add_product(product_data)
                    product_blockchain.save_chain("data/product_chain.json")
                    print(f"  [✓] Added product: {product_id} in {market}")

                    for _, row in market_rows.iterrows():
                        transaction = Transaction(
                            product_id=product_id,
                            price=float(row["Modal_Price"]),
                            private_key=private_key
                        )
                        blockchain.add_block([transaction.to_dict()], public_key)
                        blockchain.save_chain("data/transaction_chain.json")

                save_imported_file(file_name)
                print(f"[DONE] Finished importing {file_name}")

            except Exception as e:
                print(f"[ERROR] Failed to process {file_name}: {e}")

    except Exception as e:
        print(f"[ERROR] Failed to import CSV data: {e}")

### ----------------------- UI ROUTES -----------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_transaction", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        data = request.form
        try:
            transaction = Transaction(
                product_id=data["product_id"],
                price=float(data["price"]),
                private_key=private_key
            )
            blockchain.add_block([transaction.to_dict()], public_key)
            blockchain.save_chain("data/transaction_chain.json")
            return redirect(url_for("view_chain"))
        except Exception as e:
            return render_template("add_transaction.html", error=str(e))
    return render_template("add_transaction.html")

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        data = request.form
        try:
            product = Product(
                product_id=data["product_id"],
                name=data["name"],
                origin_district=data["origin_district"],
                market=data["market"]
            )
            product_blockchain.add_product(product.to_dict())
            product_blockchain.save_chain("data/product_chain.json")
            return redirect(url_for("view_chain"))
        except Exception as e:
            return render_template("add_product.html", error=str(e))
    return render_template("add_product.html")

@app.route("/view_chain", methods=["GET"])
def view_chain():
    chain_type = request.args.get("type", "transaction")
    if chain_type == "product":
        chain_data = product_blockchain.get_chain()
    else:
        chain_data = blockchain.get_chain()
    return render_template("view_chain.html", chain=chain_data, chain_type=chain_type)

@app.route("/search_transactions")
def search_transactions():
    product_id = request.args.get("product_id")
    results = []

    if product_id:
        product_info = None
        for block in product_blockchain.chain:
            for prod in block.transactions:
                if prod.get("product_id") == product_id:
                    product_info = prod
                    break

        transactions = []
        for block in blockchain.chain:
            for tx in block.transactions:
                if tx.get("product_id") == product_id:
                    transactions.append(tx)

        return render_template("search_transactions.html", product=product_info, transactions=transactions)

    return render_template("search_transactions.html", product=None, transactions=[])

@app.route("/search_product")
def search_product():
    result = None
    product_name = request.args.get("product_name")
    if product_name:
        for block in product_blockchain.chain:
            for prod in block.transactions:
                if prod["name"].lower() == product_name.lower():
                    result = prod
                    break
    return render_template("search_product.html", product=result)


@app.route("/predictions", methods=["GET", "POST"])
def predictions():
    forecast_date = request.form.get("forecast_date") or request.args.get("forecast_date") or "2026-04-05"

    try:
        parsed_date = datetime.datetime.strptime(forecast_date, "%Y-%m-%d")
        forecast_date_str = parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        forecast_date_str = "2026-04-05"

    dataset_path = os.path.join(os.path.dirname(__file__), "dataset")

    try:
        # Actually run evaluation and forecast only for APPLE.csv
        evaluation = get_model_evaluation_results(dataset_path=dataset_path)
        forecast = get_future_price_predictions(
            forecast_date_str,
            dataset_path=dataset_path,
            use_saved_models=True
        )

    except Exception as e:
        print(f"[ERROR] In prediction route: {e}")
        evaluation = []
        forecast = [{"File": "Error", "Error": str(e)}]

    return render_template(
        "predictions.html",
        evaluation=evaluation,
        forecast=forecast,
        forecast_date=forecast_date_str
    )

@app.route("/chain")
def get_chain():
    return jsonify(blockchain.get_chain())

@app.route("/product_chain")
def get_product_chain():
    return jsonify(product_blockchain.get_chain())

@app.route("/get_transactions/<product_id>")
def get_transactions_by_product(product_id):
    result = []
    for block in blockchain.chain:
        for tx in block.transactions:
            if tx.get("product_id") == product_id:
                result.append(tx)
    return jsonify(result)

@app.route("/get_product/<product_name>")
def get_product_by_name(product_name):
    for block in product_blockchain.chain:
        for prod in block.transactions:
            if prod.get("name", "").lower() == product_name.lower():
                return jsonify(prod)
    return jsonify({"error": "Product not found"}), 404

if __name__ == "__main__":
    print("[DEBUG] Starting Flask app and checking if import is needed...")
    import_excel_data_on_startup(os.path.join(os.path.dirname(__file__), "dataset"))
    app.run(debug=True)
