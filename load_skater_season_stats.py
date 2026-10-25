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
    SELECT team_id, team_name, team_abbrev
    FROM teams
""")

teams = cursor.fetchall()

team_name_map = {
    row["team_name"].lower(): row["team_id"]
    for row in teams
}


# ============================================================
# GET MAPPED SKATERS
# Goalies are excluded
# ============================================================

cursor.execute("""
    SELECT
        player_id,
        nhl_player_id,
        player_name,
        team_id,
        position
    FROM players
    WHERE nhl_player_id IS NOT NULL
      AND position <> 'G'
    ORDER BY player_id
""")

players = cursor.fetchall()

print(f"Skaters found: {len(players)}")


# ============================================================
# COUNTERS
# ============================================================

inserted = 0
skipped = 0
failed = 0


# ============================================================
# PROCESS EACH PLAYER
# ============================================================

for index, player in enumerate(players, start=1):

    nhl_player_id = player["nhl_player_id"]
    player_name = player["player_name"]

    print(
        f"[{index}/{len(players)}] "
        f"{player_name} ({nhl_player_id})"
    )

    url = (
        "https://api-web.nhle.com/v1/"
        f"player/{nhl_player_id}/landing"
    )

    try:
        response = requests.get(
            url,
            timeout=30,
        )

        response.raise_for_status()
        data = response.json()

    except Exception as error:
        failed += 1
        print(f"  API ERROR: {error}")
        continue

    season_totals = data.get("seasonTotals", [])

    # ========================================================
    # 2025-26 NHL REGULAR SEASON ONLY
    # ========================================================

    records = [
        record
        for record in season_totals
        if record.get("season") == 20252026
        and record.get("gameTypeId") == 2
        and record.get("leagueAbbrev") == "NHL"
    ]

    if not records:
        skipped += 1
        print("  No 2025-26 NHL regular-season stats")
        continue

    # ========================================================
    # PROCESS SEASON RECORD
    # ========================================================

    for record in records:

        api_team_name = (
            record.get("teamName", {})
            .get("default", "")
            .strip()
        )

        team_id = team_name_map.get(
            api_team_name.lower()
        )

        # Fallback to player's existing team
        if team_id is None:
            team_id = player["team_id"]

        if team_id is None:
            skipped += 1
            print(
                f"  Team not mapped: {api_team_name}"
            )
            continue

        season_value = str(
            record.get("season")
        )

        cursor.execute(
            """
            INSERT INTO skater_season_stats (
                player_id,
                season,
                team_id,
                games_played,
                goals,
                assists,
                points,
                plus_minus,
                penalty_min,
                shots,
                avg_toi
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
            ON DUPLICATE KEY UPDATE
                games_played = VALUES(games_played),
                goals = VALUES(goals),
                assists = VALUES(assists),
                points = VALUES(points),
                plus_minus = VALUES(plus_minus),
                penalty_min = VALUES(penalty_min),
                shots = VALUES(shots),
                avg_toi = VALUES(avg_toi)
            """,
            (
                nhl_player_id,
                season_value,
                team_id,
                record.get("gamesPlayed", 0) or 0,
                record.get("goals", 0) or 0,
                record.get("assists", 0) or 0,
                record.get("points", 0) or 0,
                record.get("plusMinus", 0) or 0,
                record.get("pim", 0) or 0,
                record.get("shots", 0) or 0,
                record.get("avgToi"),
            ),
        )

        inserted += 1

    conn.commit()
    time.sleep(0.1)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n================================")
print("SKATER SEASON STATS COMPLETE")
print("================================")
print(f"Players processed: {len(players)}")
print(f"Rows inserted/updated: {inserted}")
print(f"Players skipped: {skipped}")
print(f"Failed API requests: {failed}")


cursor.close()
conn.close()
