
from db import get_db_connection

connection = get_db_connection()
cursor = connection.cursor()

try:
    create_table_query = """
    CREATE TABLE IF NOT EXISTS teams (
        team_id INT AUTO_INCREMENT PRIMARY KEY,
        team_name VARCHAR(100) NOT NULL UNIQUE,
        wins INT,
        losses INT,
        ot_losses INT,
        points INT,
        goals_for INT,
        goals_against INT,
        games_played INT
    )
    """

    cursor.execute(create_table_query)
    connection.commit()

    print("teams table created successfully!")

finally:
    cursor.close()
    connection.close()
