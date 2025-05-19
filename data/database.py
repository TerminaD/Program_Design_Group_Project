import sqlite3


class DatabaseManager:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def initialize(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY,
                title TEXT,
                due_date TEXT
            )
        """
        )
        self.conn.commit()

    def get_assignments(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT title, due_date FROM assignments ORDER BY due_date")
        return cursor.fetchall()

    def save_assignments(self, items):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM assignments")
        cursor.executemany(
            "INSERT INTO assignments (title, due_date) VALUES (?, ?)", items
        )
        self.conn.commit()
