import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np


class CostPredictor:

    def predict(self, history):

        if len(history) < 2:
            return None

        df = pd.DataFrame(history)

        X = np.arange(len(df)).reshape(-1, 1)
        y = df["cost"]

        model = LinearRegression()
        model.fit(X, y)

        future = np.array([[len(df)]])
        prediction = model.predict(future)[0]

        return round(float(prediction), 5)