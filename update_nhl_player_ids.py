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
# GET ALL TEAMS
# ============================================================

cursor.execute(
    """
    SELECT
        team_id,
        team_name,
        team_abbrev
    FROM teams
    ORDER BY team_id
    """
)

teams = cursor.fetchall()

print(f"Teams found: {len(teams)}")


# ============================================================
# COUNTERS
# ============================================================

matched = 0
not_matched = 0
api_players = 0


# ============================================================
# PROCESS EACH TEAM
# ============================================================

for team in teams:

    team_id = team["team_id"]
    team_name = team["team_name"]
    team_abbrev = team["team_abbrev"]

    print(
        f"\nProcessing: "
        f"{team_name} ({team_abbrev})"
    )

    url = (
        "https://api-web.nhle.com/v1/"
        f"roster/{team_abbrev}/current"
    )

    try:

        response = requests.get(
            url,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

    except Exception as error:

        print(
            f"API ERROR for {team_abbrev}: "
            f"{error}"
        )

        continue

    # NHL API separates roster into these groups
    roster = []

    roster.extend(
        data.get("forwards", [])
    )

    roster.extend(
        data.get("defensemen", [])
    )

    roster.extend(
        data.get("goalies", [])
    )

    print(
        f"API players found: {len(roster)}"
    )

    api_players += len(roster)

    # ========================================================
    # PROCESS PLAYERS
    # ========================================================

    for player in roster:

        nhl_player_id = player.get("id")

        first_name = (
            player.get("firstName", {})
            .get("default", "")
            .strip()
        )

        last_name = (
            player.get("lastName", {})
            .get("default", "")
            .strip()
        )

        player_name = (
            f"{first_name} {last_name}"
        ).strip()

        if not nhl_player_id or not player_name:
            continue

        # ----------------------------------------------------
        # MATCH USING NAME + TEAM
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                player_id,
                player_name
            FROM players
            WHERE team_id = %s
              AND LOWER(TRIM(player_name))
                  = LOWER(TRIM(%s))
            LIMIT 1
            """,
            (
                team_id,
                player_name,
            ),
        )

        existing_player = cursor.fetchone()

        if existing_player:

            cursor.execute(
                """
                UPDATE players
                SET nhl_player_id = %s
                WHERE player_id = %s
                """,
                (
                    nhl_player_id,
                    existing_player["player_id"],
                ),
            )

            matched += 1

            print(
                f"  MATCHED: "
                f"{player_name} "
                f"-> {nhl_player_id}"
            )

        else:

            not_matched += 1

            print(
                f"  NOT MATCHED: "
                f"{player_name}"
            )

    # Save after each team
    conn.commit()

    # Small API delay
    time.sleep(0.2)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n================================")
print("UPDATE COMPLETE")
print("================================")

print(
    f"API players processed: "
    f"{api_players}"
)

print(
    f"Matched: {matched}"
)

print(
    f"Not matched: {not_matched}"
)


# ============================================================
# VERIFY DATABASE
# ============================================================

cursor.execute(
    """
    SELECT
        COUNT(*) AS total,
        COUNT(nhl_player_id) AS with_nhl_id
    FROM players
    """
)

result = cursor.fetchone()

print(
    f"\nDatabase players: "
    f"{result['total']}"
)

print(
    f"Players with NHL ID: "
    f"{result['with_nhl_id']}"
)


cursor.close()
conn.close()
