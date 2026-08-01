import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

class Config:

    OPENCOST_URL = os.getenv(
        "OPENCOST_URL",
        "http://localhost:9091"
    )

    DATABASE_NAME = os.getenv(
        "DATABASE_NAME",
        "cloudwarden.db"
    )

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )

    COST_THRESHOLD = float(
        os.getenv(
            "COST_THRESHOLD",
            "0.30"
        )
    )

    REFRESH_INTERVAL = int(
        os.getenv(
            "REFRESH_INTERVAL",
            "60"
        )
    )