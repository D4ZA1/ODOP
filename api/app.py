import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, jsonify, request

from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction
from security.key_generation import generate_keys

app = Flask(__name__)







private_key, public_key = generate_keys()

blockchain = Blockchain()

sample_transactions = [
    {
        "product": "Tomato",
        "district": "Mysuru",
        "price": 25.0,
        "quality_score": 0.8,
        "buyer": "RetailerA",
        "seller": "FarmerX"
    },
    {
        "product": "Onion",
        "district": "Mandya",
        "price": 20.5,
        "quality_score": 0.9,
        "buyer": "RetailerB",
        "seller": "FarmerY"
    }
]

transactions = [
    Transaction(**tx, private_key=private_key).to_dict() for tx in sample_transactions
]
blockchain.add_block(transactions, public_key)
@app.route("/")
def index():
    return jsonify({"message": "Test blockchain with dummy transactions is running."})

@app.route("/chain")
def get_chain():
    return jsonify(blockchain.get_chain())

@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    data = request.json

    required_fields = ["product", "district", "price", "quality_score", "buyer", "seller"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required transaction fields"}), 400

    # Create a new transaction from request data
    transaction = Transaction(
        product=data["product"],
        district=data["district"],
        price=data["price"],
        quality_score=data["quality_score"],
        buyer=data["buyer"],
        seller=data["seller"],
        private_key=private_key
    )

    # Add it as a new block (you can group transactions if needed)
    blockchain.add_block([transaction.to_dict()], public_key)

    return jsonify({"message": "Transaction added to blockchain!"}), 201



if __name__ == "__main__":
    app.run(debug=True)

