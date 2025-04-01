
import json

from ai_model.ai_model import AIModel
from Crypto.PublicKey import RSA
from flask import Flask, jsonify, request

from blockchain.blockchain import Blockchain

app = Flask(__name__)


blockchain = Blockchain()
ai_model = AIModel()

# Load keys
with open("public_key.pem", "rb") as pub_file:
    public_key = RSA.import_key(pub_file.read())

# Endpoint to create a new transaction
@app.route('/transaction', methods=['POST'])
def create_transaction():
    data = request.get_json()

    transaction = Transaction(
        product_id=data['product_id'],
        product_name=data['product_name'],
        producer=data['producer'],
        price=data['price'],
        category=data['category'],
        quality_rating=data['quality_rating'],
        demand_score=data['demand_score']
    )

    transaction.sign_transaction(private_key)
    blockchain.add_transaction(transaction)
    
    return jsonify({"message": "Transaction added", "transaction": data})

# Endpoint to mine a new block
@app.route('/mine', methods=['GET'])
def mine_block():
    blockchain.mine_block()
    return jsonify({"message": "New block mined", "blockchain": blockchain.chain})

# Endpoint to predict demand using AI model
@app.route('/predict', methods=['POST'])
def predict_demand():
    data = request.get_json()
    prediction = ai_model.predict_demand(data['product_data'])
    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(debug=True)
