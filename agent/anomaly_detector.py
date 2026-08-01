import pandas as pd


class AnomalyDetector:

    def detect(self, history):

        if len(history) < 5:
            return []

        df = pd.DataFrame(history)

        mean = df["cost"].mean()
        std = df["cost"].std()

        upper = mean + (2 * std)
        lower = mean - (2 * std)

        anomalies = df[
            (df["cost"] > upper) |
            (df["cost"] < lower)
        ]

        return anomalies.to_dict("records")