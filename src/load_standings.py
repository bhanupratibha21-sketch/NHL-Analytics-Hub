import requests
import mysql.connector
import streamlit as st
import pandas as pd
import plotly.express as px

from src.db import get_db_connection


# --------------------------------------------------
# Configuration
# --------------------------------------------------

API_URL = "https://api-web.nhle.com/v1/standings/now"


conn = get_db_connection()
cursor = conn.cursor()

# --------------------------------------------------
# Fetch NHL standings
# --------------------------------------------------

def fetch_standings():
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    return data["standings"]


# --------------------------------------------------
# Load standings into MySQL
# --------------------------------------------------

def load_standings(standings_data):

    connection = mysql.connector.connect(**conn.get_db_connection()._kwargs)
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO standings (
            team_id,
            season,
            games_played,
            wins,
            losses,
            ot_losses,
            points,
            goals_for,
            goals_against,
            home_wins,
            away_wins,
            streak_type,
            streak_count
        )
        SELECT
            team_id,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        FROM teams
        WHERE team_abbrev = %s
    """

    for row in standings_data:

        team_abbrev = row.get("teamAbbrev", {}).get("default")

        values = (
            "20252026",
            row.get("gamesPlayed"),
            row.get("wins"),
            row.get("losses"),
            row.get("otLosses"),
            row.get("points"),
            row.get("goalFor"),
            row.get("goalAgainst"),
            row.get("homeWins"),
            row.get("roadWins"),
            row.get("streakCode"),
            row.get("streakCount"),
            team_abbrev
        )

        cursor.execute(insert_query, values)

    connection.commit()

    print(f"Inserted {cursor.rowcount} standings records.")

    cursor.close()
    connection.close()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    standings = fetch_standings()

    print(f"Fetched {len(standings)} teams from NHL API.")

    load_standings(standings)

    print("Standings data loaded successfully.")