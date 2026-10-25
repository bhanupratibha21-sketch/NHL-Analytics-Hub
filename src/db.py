
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pintu062",
        database="nhl_analytics"
    )
conn = get_db_connection()
cursor = conn.cursor()