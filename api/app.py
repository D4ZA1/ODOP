
import os
import sys

from flask import Flask, jsonify, request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))







from blockchain.product import Product
from blockchain.product_blockchain import ProductBlockchain
from blockchain.transaction import Transaction
from blockchain.transaction_blockchain import TransactionBlockchain
from security.key_generation import generate_keys

app = Flask(__name__)







private_key, public_key = generate_keys()

# Blockchains
blockchain = TransactionBlockchain()
product_blockchain = ProductBlockchain()

# Sample data
sample_transactions = [
    {"product_id": "P001", "price": 25.0, "buyer": "RetailerA", "seller": "FarmerX"},
    {"product_id": "P002", "price": 20.5, "buyer": "RetailerB", "seller": "FarmerY"}
]

transactions = [Transaction(**tx, private_key=private_key).to_dict() for tx in sample_transactions]
blockchain.add_block(transactions, public_key)

@app.route("/")
def index():
    return jsonify({"message": "Dual blockchain for ODOP is running."})

@app.route("/chain")
def get_chain():
    return jsonify(blockchain.get_chain())

@app.route("/product_chain")
def get_product_chain():
    return jsonify(product_blockchain.get_chain())

@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    data = request.json
    required_fields = ["product_id", "price", "buyer", "seller"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required transaction fields"}), 400

    try:
        transaction = Transaction(
            product_id=data["product_id"],
            price=data["price"],
            buyer=data["buyer"],
            seller=data["seller"],
            private_key=private_key
        )
        blockchain.add_block([transaction.to_dict()], public_key)
        return jsonify({"message": "Transaction added to blockchain!"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/add_product", methods=["POST"])
def add_product():
    data = request.json

    required_fields = ["product_id", "name", "category", "origin_district"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields in request"}), 400

    product = Product(
        product_id=data["product_id"],
        name=data["name"],
        category=data["category"],
        origin_district=data["origin_district"],
        quality_score=data.get("quality_score")
    )

    product_blockchain.add_product(product.to_dict())
    return jsonify({"message": "Product metadata added to blockchain!"}), 201

@app.route("/get_transactions/<product_id>", methods=["GET"])
def get_transactions_by_product(product_id):
    result = []
    for block in blockchain.chain[1:]:  # Skip genesis block
        for tx in block.transactions:
            if tx["product_id"] == product_id:
                result.append(tx)
    return jsonify(result)

@app.route("/get_product/<product_name>", methods=["GET"])
def get_product_by_name(product_name):
    for block in product_blockchain.chain[1:]:  # Skip genesis block
        for prod in block.transactions:
            if prod["name"] == product_name:
                return jsonify(prod)
    return jsonify({"error": "Product not found"}), 404

@app.route("/search_transactions", methods=["GET"])
def search_transactions():
    buyer = request.args.get("buyer")
    seller = request.args.get("seller")
    result = []

    for block in blockchain.chain[1:]:  # Skip genesis
        for tx in block.transactions:
            if (not buyer or tx.get("buyer") == buyer) and (not seller or tx.get("seller") == seller):
                result.append(tx)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

