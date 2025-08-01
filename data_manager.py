import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path: str = "expenses.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._initialize_database()

    def _initialize_database(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def add_expense(self, amount: float, description: str, category: str):
        timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (date, amount, description, category) VALUES (?, ?, ?, ?)",
            (timestamp, amount, description, category)
        )
        self.conn.commit()

    def get_expenses(self, category: str = None, limit: int = None):
        cursor = self.conn.cursor()
        query = "SELECT date, amount, description, category FROM expenses"
        params = []

        if category:
            query += " WHERE category = ?"
            params.append(category)

        query += " ORDER BY date DESC"

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def get_summary(self, period: str = "daily"):
        cursor = self.conn.cursor()

        if period == "daily":
            cursor.execute(
                """
                SELECT category, SUM(amount) AS total
                FROM expenses
                WHERE date(date) = date('now', 'localtime')
                GROUP BY category
                """
            )
        elif period == "monthly":
            cursor.execute(
                """
                SELECT category, SUM(amount) AS total
                FROM expenses
                WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now', 'localtime')
                GROUP BY category
                """
            )
        else:
            raise ValueError(f"Unknown period: {period}")

        rows = cursor.fetchall()
        return {row['category']: row['total'] for row in rows}

