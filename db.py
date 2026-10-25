
import os
import mysql.connector

def get_db_connection():
    password = os.getenv("NHL_DB_PASSWORD")

    if not password:
        raise RuntimeError("NHL_DB_PASSWORD environment variable is not set")

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="nhl_analytics"
    )
