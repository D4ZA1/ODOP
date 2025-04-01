import numpy as np
from sklearn.ensemble import RandomForestClassifier


def train_quality_model(data):


    X = np.array(data['features'])
    y = np.array(data['labels'])
    model = RandomForestClassifier().fit(X, y)
    return model

def predict_quality(model, features):
    return model.predict([features])[0]
