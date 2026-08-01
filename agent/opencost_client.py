import requests

from config import Config
from logger import logger


class OpenCostClient:
    """
    Client for communicating with the OpenCost API.
    """

    def __init__(self):
        self.base_url = Config.OPENCOST_URL.rstrip("/")

    def health_check(self):
        """
        Check whether the OpenCost API is reachable.
        """

        try:
            response = requests.get(
                f"{self.base_url}/healthz",
                timeout=10
            )

            response.raise_for_status()

            logger.info("OpenCost health check successful.")

            return True

        except requests.RequestException as error:

            logger.error(
                f"OpenCost health check failed: {error}"
            )

            return False

    def get_allocations(self, window="today"):
        """
        Fetch allocation data from OpenCost.
        """

        url = f"{self.base_url}/model/allocation"

        params = {
            "window": window
        }

        try:

            response = requests.get(
                url,
                params=params,
                timeout=20
            )

            response.raise_for_status()

            data = response.json()

            if "data" not in data:

                logger.warning(
                    "Allocation response does not contain 'data'."
                )

                return {}

            allocations = data["data"][0]

            logger.info(
                f"Fetched {len(allocations)} workloads from OpenCost."
            )

            return allocations

        except requests.RequestException as error:

            logger.error(
                f"Unable to retrieve allocation data: {error}"
            )

            return {}

        except Exception as error:

            logger.exception(
                f"Unexpected error while reading allocation data: {error}"
            )

            return {}