
import numpy as np
from sklearn.linear_model import LinearRegression


def train_price_model(data):

    X = np.array(data['features']).reshape(-1, 1)
    y = np.array(data['prices'])
    model = LinearRegression().fit(X, y)
    return model

def predict_price(model, feature):
    return model.predict([[feature]])[0]
