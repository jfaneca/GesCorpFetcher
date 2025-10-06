import sqlite3
from app.logger import Logger
from pathlib import Path

DB_FILE = 'GescorpFetcher.db'

class DBClient:
    def __init__(self, logger:Logger):
        file_path = Path(DB_FILE)

        initialize_db_required = False

        if not file_path.exists():
            initialize_db_required = True
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.logger = logger.get_logger()
        if initialize_db_required:
            self.initialize_db()

    def initialize_db(self):
        # Create a table named 'tasks'
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY,
                created_at TIMESTAMP NOT NULL
            )
        ''')

        # Save changes and close the connection
        self.conn.commit()
        self.conn.close()
        print(f"Database '{DB_FILE}' and 'alerts' table initialized.")

    def insert_record(self, id):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()

        # Use '?' as placeholders to prevent SQL injection (best practice)
        self.cursor.execute(
            "INSERT INTO alerts (id, created_at) VALUES (?, datetime('now', 'localtime'))",
            (id,)
        )

        self.conn.commit()
        self.conn.close()
        print(f"record with id '{id}' created.")

    def get_all_alerts(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * FROM alerts ORDER BY created_at DESC")
        alerts = self.cursor.fetchall()

        self.conn.close()
        return alerts

if __name__ == "__main__":
    db_client = DBClient()
    db_client.initialize_db()
