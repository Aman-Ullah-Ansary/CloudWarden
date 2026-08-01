import sqlite3
import bcrypt


class Auth:

    def __init__(self):

        self.conn = sqlite3.connect(
            "cloudwarden.db",
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT
        )
        """)

        self.conn.commit()

    def register(self, username, email, password):

        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        try:

            self.cursor.execute(
                """
                INSERT INTO users(username,email,password)
                VALUES(?,?,?)
                """,
                (username, email, hashed)
            )

            self.conn.commit()

            return True, "Registration Successful"

        except sqlite3.IntegrityError:

            return False, "Username or Email already exists"

    def login(self, username, password):

        self.cursor.execute(
            """
            SELECT password
            FROM users
            WHERE username=?
            """,
            (username,)
        )

        row = self.cursor.fetchone()

        if row is None:

            return False

        stored = row[0].encode()

        return bcrypt.checkpw(
            password.encode(),
            stored
        )