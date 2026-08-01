from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, Histogram, generate_latest
import sqlite3
import pandas as pd
import time

app = FastAPI(
    title="CloudWarden AI API",
    version="2.0"
)

REQUEST_COUNT = Counter(
    "cloudwarden_requests_total",
    "Total API Requests",
    ["endpoint"]
)

REQUEST_TIME = Histogram(
    "cloudwarden_request_duration_seconds",
    "Request Duration",
    ["endpoint"]
)


@app.get("/")
def home():

    REQUEST_COUNT.labels("/").inc()

    start = time.time()

    result = {
        "message": "CloudWarden AI API Running"
    }

    REQUEST_TIME.labels("/").observe(
        time.time() - start
    )

    return result


@app.get("/costs")
def costs():

    REQUEST_COUNT.labels("/costs").inc()

    start = time.time()

    conn = sqlite3.connect(
        "cloudwarden.db"
    )

    df = pd.read_sql(
        "SELECT * FROM namespace_costs",
        conn
    )

    conn.close()

    REQUEST_TIME.labels("/costs").observe(
        time.time() - start
    )

    return df.to_dict(
        orient="records"
    )


@app.get("/forecast")
def forecast():

    REQUEST_COUNT.labels("/forecast").inc()

    start = time.time()

    conn = sqlite3.connect(
        "cloudwarden.db"
    )

    df = pd.read_sql(
        """
        SELECT *
        FROM forecasts
        ORDER BY id DESC
        LIMIT 1
        """,
        conn
    )

    conn.close()

    REQUEST_TIME.labels("/forecast").observe(
        time.time() - start
    )

    return df.to_dict(
        orient="records"
    )


@app.get(
    "/metrics",
    response_class=PlainTextResponse
)
def metrics():

    return generate_latest().decode("utf-8")