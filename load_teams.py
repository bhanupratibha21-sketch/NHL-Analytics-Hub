import pandas as pd
import mysql.connector

# Load standings data
df = pd.read_csv("data/raw/standings.csv")

# Connect to MySQL
import os
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("NHL_DB_PASSWORD"),
    database="nhl_analytics"
)

cursor = connection.cursor()

# SQL insert query
insert_query = """
INSERT INTO teams (
    team_name,
    wins,
    losses,
    ot_losses,
    points,
    goals_for,
    goals_against,
    games_played
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    wins = VALUES(wins),
    losses = VALUES(losses),
    ot_losses = VALUES(ot_losses),
    points = VALUES(points),
    goals_for = VALUES(goals_for),
    goals_against = VALUES(goals_against),
    games_played = VALUES(games_played)
"""

# Convert DataFrame rows into tuples
data = [
    (
        row["team"],
        row["wins"],
        row["losses"],
        row["ot_losses"],
        row["points"],
        row["goals_for"],
        row["goals_against"],
        row["games_played"]
    )
    for _, row in df.iterrows()
]

# Insert teams into MySQL
cursor.executemany(insert_query, data)

# Save changes
connection.commit()

print(f"{cursor.rowcount} teams inserted successfully!")

# Close connection
cursor.close()
connection.close()