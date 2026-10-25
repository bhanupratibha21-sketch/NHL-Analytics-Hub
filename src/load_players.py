import requests
import mysql.connector
from src.db import get_db_connection


# --------------------------------------------------
# Database connection
# --------------------------------------------------


conn = get_db_connection()
cursor = conn.cursor()

cursor = conn.cursor()


# --------------------------------------------------
# Fetch NHL teams
# --------------------------------------------------

teams_url = "https://api-web.nhle.com/v1/standings/now"

response = requests.get(teams_url)
response.raise_for_status()

standings_data = response.json()


# --------------------------------------------------
# Fetch roster for each team
# --------------------------------------------------

for team in standings_data["standings"]:

    team_abbrev = team["teamAbbrev"]["default"]

    # Find team_id from MySQL
    cursor.execute(
        "SELECT team_id FROM teams WHERE team_abbrev = %s",
        (team_abbrev,)
    )

    result = cursor.fetchone()

    if not result:
        print(f"Team not found: {team_abbrev}")
        continue

    team_id = result[0]

    roster_url = f"https://api-web.nhle.com/v1/roster/{team_abbrev}/current"

    roster_response = requests.get(roster_url)

    if roster_response.status_code != 200:
        print(f"Could not fetch roster for {team_abbrev}")
        continue

    roster = roster_response.json()

    # --------------------------------------------------
    # Insert forwards
    # --------------------------------------------------

    for player in roster.get("forwards", []):

        player_name = (
            player["firstName"]["default"]
            + " "
            + player["lastName"]["default"]
        )

        position = player.get("positionCode")
        jersey_number = player.get("sweaterNumber")

        cursor.execute(
            """
            INSERT INTO players
            (player_name, team_id, position, jersey_number)
            VALUES (%s, %s, %s, %s)
            """,
            (
                player_name,
                team_id,
                position,
                jersey_number
            )
        )

    # --------------------------------------------------
    # Insert defensemen
    # --------------------------------------------------

    for player in roster.get("defensemen", []):

        player_name = (
            player["firstName"]["default"]
            + " "
            + player["lastName"]["default"]
        )

        position = player.get("positionCode")
        jersey_number = player.get("sweaterNumber")

        cursor.execute(
            """
            INSERT INTO players
            (player_name, team_id, position, jersey_number)
            VALUES (%s, %s, %s, %s)
            """,
            (
                player_name,
                team_id,
                position,
                jersey_number
            )
        )

    # --------------------------------------------------
    # Insert goalies
    # --------------------------------------------------

    for player in roster.get("goalies", []):

        player_name = (
            player["firstName"]["default"]
            + " "
            + player["lastName"]["default"]
        )

        position = player.get("positionCode")
        jersey_number = player.get("sweaterNumber")

        cursor.execute(
            """
            INSERT INTO players
            (player_name, team_id, position, jersey_number)
            VALUES (%s, %s, %s, %s)
            """,
            (
                player_name,
                team_id,
                position,
                jersey_number
            )
        )

    print(f"Loaded players for {team_abbrev}")


# --------------------------------------------------
# Commit changes
# --------------------------------------------------

conn.commit()

cursor.close()
conn.close()

print("Player data loaded successfully.")