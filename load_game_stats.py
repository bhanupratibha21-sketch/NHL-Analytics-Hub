import time

import mysql.connector
import requests


# ============================================================
# DATABASE CONNECTION
# ============================================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",

    database="nhl_analytics",
)

cursor = conn.cursor(dictionary=True)


# ============================================================
# GET TEAM MAPPING
# ============================================================

cursor.execute("""
    SELECT team_id, team_abbrev
    FROM teams
""")

team_map = {
    row["team_abbrev"]: row["team_id"]
    for row in cursor.fetchall()
}


# ============================================================
# GET VALID NHL PLAYER IDS
# ============================================================

cursor.execute("""
    SELECT nhl_player_id
    FROM players
    WHERE nhl_player_id IS NOT NULL
""")

valid_players = {
    row["nhl_player_id"]
    for row in cursor.fetchall()
}


# ============================================================
# GET GAMES
# ============================================================

cursor.execute("""
    SELECT
        game_id,
        home_team_abbrev,
        away_team_abbrev
    FROM games
    ORDER BY game_date
""")

games = cursor.fetchall()

print(f"Games found: {len(games)}")
print(f"Mapped NHL players: {len(valid_players)}")


# ============================================================
# COUNTERS
# ============================================================

inserted = 0
skipped_players = 0
failed_games = 0


# ============================================================
# PROCESS GAMES
# ============================================================

for index, game in enumerate(games, start=1):

    game_id = game["game_id"]

    print(
        f"[{index}/{len(games)}] "
        f"Processing game {game_id}"
    )

    url = (
        "https://api-web.nhle.com/v1/"
        f"gamecenter/{game_id}/boxscore"
    )

    try:
        response = requests.get(
            url,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

    except Exception as error:
        failed_games += 1
        print(f"  API ERROR: {error}")
        continue

    player_stats = data.get(
        "playerByGameStats",
        {}
    )

    # ========================================================
    # HOME + AWAY
    # ========================================================

    for side in ["awayTeam", "homeTeam"]:

        team_data = player_stats.get(
            side,
            {}
        )

        if side == "awayTeam":
            team_abbrev = game["away_team_abbrev"]
        else:
            team_abbrev = game["home_team_abbrev"]

        team_id = team_map.get(team_abbrev)

        if team_id is None:
            print(
                f"  Team not found: {team_abbrev}"
            )
            continue

        # ====================================================
        # SKATERS ONLY
        # ====================================================

        skaters = []

        skaters.extend(
            team_data.get("forwards", [])
        )

        skaters.extend(
            team_data.get("defense", [])
        )

        for player in skaters:

            nhl_player_id = player.get(
                "playerId"
            )

            if nhl_player_id not in valid_players:
                skipped_players += 1
                continue

            goals = player.get("goals", 0) or 0
            assists = player.get("assists", 0) or 0
            points = player.get("points", 0) or 0

            shots_on_goal = (
                player.get("sog", 0) or 0
            )

            penalty_min = (
                player.get("pim", 0) or 0
            )

            toi = player.get("toi")

            plus_minus = (
                player.get("plusMinus", 0) or 0
            )

            cursor.execute(
                """
                INSERT INTO game_stats (
                    game_id,
                    player_id,
                    team_id,
                    goals,
                    assists,
                    points,
                    shots_on_goal,
                    penalty_min,
                    toi,
                    plus_minus
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
                """,
                (
                    game_id,
                    nhl_player_id,
                    team_id,
                    goals,
                    assists,
                    points,
                    shots_on_goal,
                    penalty_min,
                    toi,
                    plus_minus,
                ),
            )

            inserted += 1

    # Commit after each game
    conn.commit()

    # Small delay between NHL requests
    time.sleep(0.1)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n================================")
print("GAME STATS LOAD COMPLETE")
print("================================")

print(f"Games processed: {len(games)}")
print(f"Rows inserted: {inserted}")
print(f"Players skipped: {skipped_players}")
print(f"Failed games: {failed_games}")


cursor.close()
conn.close()
