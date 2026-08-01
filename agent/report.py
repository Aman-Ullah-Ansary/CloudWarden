from utils import print_header


class ReportGenerator:

    def display(self, result):

        analysis = result["analysis"]

        print_header("CloudWarden AI Executive Report")

        total_cost = sum(
            item["cost"] for item in analysis
        )

        print(f"Total Namespaces : {len(analysis)}")
        print(f"Cluster Cost     : ${total_cost:.5f}")

        highest = max(
            analysis,
            key=lambda x: x["cost"]
        )

        print(f"Highest Cost     : {highest['namespace']}")
        print(f"Highest Amount   : ${highest['cost']:.5f}")

        print()

        print("-" * 70)
        print("Namespace Summary")
        print("-" * 70)

        for item in analysis:

            print(
                f"{item['namespace']:<20}"
                f"${item['cost']:<12.5f}"
                f"{item['change']:>8.2f}%"
            )

        print()

        print("-" * 70)
        print("AI Recommendations")
        print("-" * 70)

        for item in analysis:

            print(f"\n[{item['namespace']}]")

            for recommendation in item["recommendation"]:

                print(item["recommendation"])

        print()