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
# TEAM MAPPING
# ============================================================

cursor.execute("""
    SELECT team_id, team_name
    FROM teams
""")

teams = cursor.fetchall()

team_name_map = {
    row["team_name"].lower(): row["team_id"]
    for row in teams
}


# ============================================================
# GET GOALIES
# ============================================================

cursor.execute("""
    SELECT
        player_id,
        nhl_player_id,
        player_name,
        team_id
    FROM players
    WHERE position = 'G'
      AND nhl_player_id IS NOT NULL
    ORDER BY player_id
""")

goalies = cursor.fetchall()

print(f"Goalies found: {len(goalies)}")


inserted = 0
skipped = 0
failed = 0


# ============================================================
# PROCESS EACH GOALIE
# ============================================================

for index, goalie in enumerate(goalies, start=1):

    nhl_player_id = goalie["nhl_player_id"]
    player_name = goalie["player_name"]

    print(
        f"[{index}/{len(goalies)}] "
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

    # 2025-26 NHL regular season only
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

    for record in records:

        api_team_name = (
            record.get("teamName", {})
            .get("default", "")
            .strip()
        )

        team_id = team_name_map.get(
            api_team_name.lower()
        )

        # Fallback to current player team
        if team_id is None:
            team_id = goalie["team_id"]

        if team_id is None:
            skipped += 1
            print(f"  Team not mapped: {api_team_name}")
            continue

        shots_against = record.get("shotsAgainst", 0) or 0
        goals_against = record.get("goalsAgainst", 0) or 0

        # NHL landing response does not provide saves directly
        saves = max(0, shots_against - goals_against)

        cursor.execute(
            """
            INSERT INTO goalie_season_stats (
                player_id,
                season,
                team_id,
                games_played,
                wins,
                losses,
                ot_losses,
                save_pct,
                goals_against_avg,
                shutouts,
                saves
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
            ON DUPLICATE KEY UPDATE
                games_played = VALUES(games_played),
                wins = VALUES(wins),
                losses = VALUES(losses),
                ot_losses = VALUES(ot_losses),
                save_pct = VALUES(save_pct),
                goals_against_avg = VALUES(goals_against_avg),
                shutouts = VALUES(shutouts),
                saves = VALUES(saves)
            """,
            (
                nhl_player_id,
                str(record.get("season")),
                team_id,
                record.get("gamesPlayed", 0) or 0,
                record.get("wins", 0) or 0,
                record.get("losses", 0) or 0,
                record.get("otLosses", 0) or 0,
                record.get("savePctg"),
                record.get("goalsAgainstAvg"),
                record.get("shutouts", 0) or 0,
                saves,
            ),
        )

        inserted += 1

    conn.commit()
    time.sleep(0.1)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n================================")
print("GOALIE SEASON STATS COMPLETE")
print("================================")
print(f"Goalies processed: {len(goalies)}")
print(f"Rows inserted/updated: {inserted}")
print(f"Goalies skipped: {skipped}")
print(f"Failed API requests: {failed}")


cursor.close()
conn.close()
