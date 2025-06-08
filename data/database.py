import sqlite3


class DatabaseManager:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        
    def delete_all_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS assignments")
        cursor.execute("DROP TABLE IF EXISTS exams")
        self.conn.commit()

    def initialize(self):
        cursor = self.conn.cursor()
        cursor.execute(  # Source: scraper, user
            """
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY,
                subject TEXT,
                content TEXT,
                due_date TEXT,
                source TEXT
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS exams (
                id INTEGER PRIMARY KEY,
                subject TEXT,
                due_date TEXT
            );
        """
        )
        self.conn.commit()

    def get_assignments(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT subject, content, due_date FROM assignments")
        return cursor.fetchall()

    def get_exams(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT subject, due_date FROM exams")
        return cursor.fetchall()

    def add_assignment(self, subject: str, content: str, due_date: str, source: str):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO assignments (subject, content, due_date, source) VALUES (?, ?, ?, ?)",
            (subject, content, due_date, source),
        )
        self.conn.commit()

    def add_exam(self, subject: str, due_date: str):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO exams (subject, due_date) VALUES (?, ?)",
            (subject, due_date),
        )
        self.conn.commit()

    def delete_assignment(self, id: int):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM assignments WHERE id = ?", (id,))
        self.conn.commit()

    def delete_exam(self, id: int):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM exams WHERE id = ?", (id,))
        self.conn.commit()

    def delete_all_scraper_assignments(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM assignments WHERE source = 'scraper'")
        self.conn.commit()
