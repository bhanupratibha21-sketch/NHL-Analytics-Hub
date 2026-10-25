import pandas as pd
import mysql.connector

# Load cleaned games data
df = pd.read_csv("data/games_cleaned.csv")

# Convert game_date to date format
df["game_date"] = pd.to_datetime(df["game_date"]).dt.date

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",

    database="nhl_analytics"
)

cursor = connection.cursor()

# SQL insert query
insert_query = """
INSERT INTO games (
    game_id,
    season,
    game_type,
    game_date,
    home_team_abbrev,
    away_team_abbrev,
    home_score,
    away_score,
    game_state,
    venue_name
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Convert DataFrame rows into tuples
data = [
    (
        row["game_id"],
        row["season"],
        row["game_type"],
        row["game_date"],
        row["home_team_abbrev"],
        row["away_team_abbrev"],
        row["home_score"],
        row["away_score"],
        row["game_state"],
        row["venue_name"]
    )
    for _, row in df.iterrows()
]

# Insert all records
cursor.executemany(insert_query, data)

# Save changes
connection.commit()

print(f"{cursor.rowcount} games inserted successfully!")

# Close connection
cursor.close()
connection.close()
