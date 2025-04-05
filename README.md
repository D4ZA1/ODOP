# Blockchain-Based Price Prediction System with ML Integration

## Overview

This project is a **Blockchain-based Price Prediction System** aimed at predicting agricultural product prices and ensuring secure transaction recording through a blockchain. The system integrates **Machine Learning (ML)** models to predict prices and assess the quality of products. It uses **RSA encryption** for secure transactions. The system processes data from the **CFTRI PMFME (One District One Product - ODOP)** database and can generate synthetic prices for products where real data is not available.

The project includes:
- A blockchain to store transactions related to product sales.
- Machine learning models for **price prediction** and **quality assessment**.
- RSA encryption for secure transaction processing.
- Data fetching and processing from the **CFTRI ODOP database** (with fallback to synthetic data).

## Features

1. **Blockchain Transactions**: 
   - Transactions are securely recorded on the blockchain with RSA encryption.
   - Each transaction includes the product, district, price, and quality score.

2. **Price Prediction**:
   - Uses **linear regression** to predict the price of agricultural products based on historical data.
   
3. **Quality Assessment**:
   - Uses a **Random Forest Classifier** to assess the quality of products (good or bad) based on features.
   
4. **Secure RSA Encryption**:
   - RSA keys are generated for transaction encryption and decryption.
   - Each transaction is encrypted using the public key and decrypted with the private key.

5. **CFTRI Data Integration**:
   - The project fetches agricultural product data from the CFTRI ODOP database.
   - Prices are either fetched from real data (if available) or generated synthetically.

## File Structure

The project is structured into several key modules:

blockchain_project/
│── blockchain/
│   │── __init__.py
│   │── blockchain.py        # Blockchain logic (block creation and chain management)
│   │── block.py             # Block definition (stores transaction details)
│   │── transaction.py       # Transaction logic (structure of transaction data)
│── api/
│   │── app.py               # Flask application for handling API requests (add transaction, view blockchain)
│── security/
│   │── key_generation.py    # RSA key generation logic for encryption
│── ml/
│   │── price_prediction.py  # ML model for predicting product prices
│   │── quality_assessment.py# ML model for assessing product quality
│── data/
│   │── fetch_odop_data.py   # Fetch and parse data from CFTRI ODOP website
│   │── generate_synthetic_prices.py  # Generate synthetic price data for products
│── scripts/
│   │── integrate_ml_blockchain.py  # Integrates ML models with the blockchain
│── requirements.txt         # Python dependencies
│── README.md                # Project documentation


### Key Files

- **`blockchain/block.py`**: Defines the structure of a blockchain block. Each block contains the index, previous block's hash, list of transactions, and a timestamp.
  
- **`blockchain/blockchain.py`**: Handles blockchain operations like adding blocks and generating the genesis block.

- **`blockchain/transaction.py`**: Defines the structure of a transaction, including product, district, price, quality score, buyer, and seller.

- **`api/app.py`**: Flask-based API for interacting with the blockchain. Includes routes for adding transactions and fetching the blockchain.

- **`security/key_generation.py`**: Generates RSA public and private keys for transaction encryption.

- **`ml/price_prediction.py`**: A machine learning model using **Linear Regression** to predict prices of agricultural products based on features.

- **`ml/quality_assessment.py`**: A machine learning model using **Random Forest Classifier** to assess product quality (good or bad).

- **`data/fetch_odop_data.py`**: Fetches product names from the CFTRI ODOP database and generates synthetic prices for products.

- **`data/generate_synthetic_prices.py`**: Generates synthetic price data for agricultural products based on predefined categories.

- **`scripts/integrate_ml_blockchain.py`**: Integrates ML models (price prediction and quality assessment) with the blockchain system for a seamless workflow.

## Setup Instructions

### Prerequisites

To run this project, you will need Python 3.6+ and `pip` installed.

1. Clone this repository to your local machine.

    ```bash
    git clone <repository-url>
    cd blockchain_project
    ```

2. Install required Python libraries.

    ```bash
    pip install -r requirements.txt
    ```

### Running the Project

1. **Start the Flask API server**:
   
   To start the Flask application that handles requests to add transactions and view the blockchain, run the following command:

   ```bash
   python api/app.py



## How to Interact with the Code

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone <repository-url>
cd blockchain_project


## Install Dependencies
pip install -r requirements.txt

##Running the Flask API Server
python api/app.py

##Interacting with the API

{
    "product": "Tomato",
    "district": "Karnataka",
    "price": 120,
    "quality_score": 95,
    "buyer": "John Doe",
    "seller": "Farmer A"
}

##View the Blockchain
curl http://127.0.0.1:5000/get_chain

