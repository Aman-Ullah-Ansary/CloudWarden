import sqlite3


class Database:

    def __init__(self):
        self.conn = sqlite3.connect("cloudwarden.db")
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS namespace_costs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            namespace TEXT,
            cost REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecasts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            predicted_cost REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()

    def insert_cost(self, namespace, cost):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO namespace_costs(namespace, cost)
            VALUES(?, ?)
            """,
            (namespace, cost)
        )

        self.conn.commit()

    def fetch_history(self, namespace):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT cost
            FROM namespace_costs
            WHERE namespace=?
            ORDER BY id
            """,
            (namespace,)
        )

        rows = cursor.fetchall()

        return [{"cost": row[0]} for row in rows]

    def save_forecast(self, predicted_cost):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO forecasts(predicted_cost)
            VALUES(?)
            """,
            (predicted_cost,)
        )

        self.conn.commit()

    def close(self):
        self.conn.close()