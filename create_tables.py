
from db import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

try:
    create_games_table = """
    CREATE TABLE IF NOT EXISTS games (
        game_id BIGINT PRIMARY KEY,
        season INT,
        game_type INT,
        game_date DATE,
        home_team_abbrev VARCHAR(10),
        away_team_abbrev VARCHAR(10),
        home_score INT,
        away_score INT,
        game_state VARCHAR(20),
        venue_name VARCHAR(255)
    )
    """

    cursor.execute(create_games_table)
    print("games table created successfully!")

finally:
    cursor.close()
    conn.close()
