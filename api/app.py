
from flask import Flask, jsonify, request

from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction
from data.fetch_odop_data import fetch_odop_data
from security.key_generation import generate_keys

app = Flask(__name__)

blockchain = Blockchain()
private_key, public_key = generate_keys()

# Fetch ODOP data (products and prices)
product_names, product_prices = fetch_odop_data()

@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    data = request.json
    
    # Validate if the product exists in the fetched product list
    if data["product"] not in product_names:
        return jsonify({"message": "Invalid product!"}), 400
    
    # Get the synthetic price for the product
    price = product_prices.get(data["product"])
    
    # Create the transaction with the synthetic price
    transaction = Transaction(
        product=data["product"],
        district=data["district"],
        price=price,
        quality_score=data["quality_score"],
        buyer=data["buyer"],
        seller=data["seller"],
        private_key=private_key
    )
    
    # Add transaction to blockchain after verification
    blockchain.add_block([transaction.to_dict()], public_key)
    
    return jsonify({"message": "Transaction added successfully"}), 200

@app.route("/get_chain", methods=["GET"])
def get_chain():
    return jsonify(blockchain.get_chain())

if __name__ == "__main__":
    app.run(debug=True)

