
from ml.price_prediction import train_price_model
from ml.quality_assessment import train_quality_model

from blockchain.blockchain import Blockchain


def integrate_models():

    blockchain = Blockchain()
    
    # Synthetic data for training
    price_data = {"features": [[1], [2], [3]], "prices": [100, 200, 300]}
    quality_data = {"features": [[1, 0], [0, 1]], "labels": ["good", "bad"]}
    
    price_model = train_price_model(price_data)
    quality_model = train_quality_model(quality_data)
    
    return blockchain, price_model, quality_model
