# player/bookmark_manager.py

import sqlite3
import os

class BookmarkManager:
    def __init__(self, db_path="data/bookmarks.db"):
        """Initializes the BookmarkManager with the path to the database file."""
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        """Creates the bookmarks table in the database if it doesn't exist."""
        if not os.path.exists(os.path.dirname(self.db_path)):
            os.makedirs(os.path.dirname(self.db_path))  # Create the 'data' directory if it doesn't exist

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS bookmarks (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           file_path TEXT UNIQUE,
                           position REAL
                       );
                       """)
        conn.commit()
        conn.close()

    def save_bookmark(self, file_path, position):
        """
        Saves the current position of the audiobook in the database.

        If a bookmark for the file already exists, it updates it. Otherwise, it creates a new one.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""REPLACE INTO bookmarks (file_path, position) VALUES (?, ?)""",
                       (file_path, position))  # REPLACE ensures we either insert a new row or update an existing one
        conn.commit()
        conn.close()

    def get_bookmark(self, file_path):
        """
        Retrieves the saved position for the given audiobook file.

        Returns 0.0 if no bookmark is found (i.e., the file is new or has no saved position).
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT position FROM bookmarks WHERE file_path=?", (file_path,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0.0  # Return 0.0 if no bookmark exists

    def delete_bookmark(self, file_path):
        """Deletes a bookmark for the given audiobook."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookmarks WHERE file_path=?", (file_path,))
        conn.commit()
        conn.close()

    def clear_all_bookmarks(self):
        """Clears all bookmarks from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookmarks")
        conn.commit()
        conn.close()
