from analyzer import CostAnalyzer
from report import ReportGenerator
from predictor import CostPredictor
from anomaly_detector import AnomalyDetector
from database import Database


def main():

    analyzer = CostAnalyzer()
    result = analyzer.analyze()

    if result["status"] != "healthy":
        print(result["message"])
        return

    report = ReportGenerator()
    report.display(result)

    predictor = CostPredictor()

    forecast = predictor.predict(result["analysis"])

    db = Database()

    if forecast is not None:
        db.save_forecast(forecast)

    if forecast is not None:
        print(f"\nForecast Next Cost : ${forecast:.5f}")

    detector = AnomalyDetector()

    anomalies = detector.detect(result["analysis"])

    print("\n" + "=" * 70)

    if anomalies:
        print("Anomalies Detected:")
        for item in anomalies:
            print(
                f"{item['namespace']}  ${item['cost']:.5f}"
            )
    else:
        print("No anomalies detected.")

    print("=" * 70)
    print("CloudWarden AI Agent")
    print("=" * 70)
    print(f"Status : {result['status']}")
    print(f"Message: {result['message']}")
    print("=" * 70)


if __name__ == "__main__":
    main()