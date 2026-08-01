from collections import defaultdict

from database import Database
from logger import logger
from opencost_client import OpenCostClient


class CostCollector:
    """
    Collects namespace cost information from OpenCost
    and stores it in SQLite.
    """

    def __init__(self):

        self.client = OpenCostClient()
        self.database = Database()

    def collect(self):

        logger.info("Starting cost collection...")

        allocations = self.client.get_allocations()

        if not allocations:

            logger.warning("No allocation data received.")

            return {}

        namespace_cost = defaultdict(float)

        for workload in allocations.values():

            try:

                namespace = workload["properties"]["namespace"]

                cost = float(
                    workload.get(
                        "totalCost",
                        0
                    )
                )

                namespace_cost[namespace] += cost

            except Exception as error:

                logger.error(
                    f"Skipping invalid workload: {error}"
                )

        logger.info(
            f"Discovered {len(namespace_cost)} namespaces."
        )

        for namespace, cost in namespace_cost.items():

            try:

                self.database.insert_cost(
                    namespace,
                    cost
                )

                logger.info(
                    f"Saved {namespace} -> ${cost:.5f}"
                )

            except Exception as error:

                logger.error(
                    f"Database insert failed: {error}"
                )

        return namespace_cost

    def history(self, namespace):

        return self.database.fetch_history(
            namespace
        )

    def close(self):

        self.database.close()