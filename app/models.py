import mysql.connector
from flask import current_app
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username



def get_db_connection():
    """Create and return a MySQL connection using configuration from Flask app config."""
    conn = mysql.connector.connect(
        host=current_app.config['MYSQL_HOST'],
        port=current_app.config['MYSQL_PORT'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        database=current_app.config['MYSQL_DATABASE']
    )
    return conn


class Firmware:
    """Simple data‑access class for firmware records (no ORM)."""

    @staticmethod
    def all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, version, filename, uploaded_at FROM firmware ORDER BY uploaded_at DESC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def get_latest():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM firmware ORDER BY uploaded_at DESC LIMIT 1")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    @staticmethod
    def insert(version, filename, file_path):
        conn = get_db_connection()
        cursor = conn.cursor()
        # Store file on disk, just record filename
        cursor.execute(
            "INSERT INTO firmware (version, filename, uploaded_at) VALUES (%s, %s, NOW())",
            (version, filename)
        )
        conn.commit()
        cursor.close()
        conn.close()
        # Move uploaded file into static/firmware folder (handled in route)
        return cursor.lastrowid
