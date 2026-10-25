
import os
import mysql.connector

password = os.getenv("NHL_DB_PASSWORD")

if not password:
    raise RuntimeError("NHL_DB_PASSWORD environment variable is not set")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password
)

cursor = conn.cursor()

try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS nhl_analytics")
    print("nhl_analytics database created successfully!")
finally:
    cursor.close()
    conn.close()
