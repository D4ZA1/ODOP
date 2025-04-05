import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, jsonify

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

if __name__ == "__main__":
    app.run(debug=True)

