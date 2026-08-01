from collector import CostCollector
from recommender import RecommendationEngine
from logger import logger


class CostAnalyzer:

    def __init__(self):
        self.collector = CostCollector()
        self.recommender = RecommendationEngine()

    def analyze(self):

        logger.info("Starting CloudWarden analysis...")

        namespace_cost = self.collector.collect()

        if not namespace_cost:
            return {
                "status": "error",
                "message": "No cost data available.",
                "namespace_cost": {},
                "analysis": []
            }

        sorted_namespaces = sorted(
            namespace_cost.items(),
            key=lambda x: x[1],
            reverse=True
        )

        analysis = []

        print("\n")
        print("=" * 70)
        print("CloudWarden AI Cost Analysis")
        print("=" * 70)
        print(f"\n{'Namespace':20} {'Cost($)':>12}")
        print("-" * 35)

        for namespace, cost in sorted_namespaces:

            history = self.collector.history(namespace)

            if len(history) >= 2:
                previous = history[-2]["cost"]
            else:
                previous = cost

            difference = cost - previous

            if previous > 0:
                percent_change = (difference / previous) * 100
            else:
                percent_change = 0

            recommendation = self.recommender.generate(
                namespace,
                cost
            )

            analysis.append({
                "namespace": namespace,
                "cost": cost,
                "previous": previous,
                "change": percent_change,
                "recommendation": recommendation
            })

            symbol = "⬆" if percent_change >= 0 else "⬇"

            print(
                f"{namespace:20}"
                f"${cost:10.5f} "
                f"{symbol} {percent_change:7.2f}%"
            )

        print()

        highest = analysis[0]

        print("=" * 70)
        print("Highest Cost Namespace")
        print("=" * 70)
        print(f"Namespace      : {highest['namespace']}")
        print(f"Current Cost   : ${highest['cost']:.5f}")
        print(f"Previous Cost  : ${highest['previous']:.5f}")
        print(f"Change         : {highest['change']:.2f}%")

        print("\nRecommendations")
        print("-" * 70)
        print(highest["recommendation"])

        return {
            "status": "healthy",
            "message": f"Analyzed {len(namespace_cost)} namespaces.",
            "namespace_cost": namespace_cost,
            "analysis": analysis
        }