import streamlit as st
import os
import pandas as pd

import mysql.connector

import plotly.express as px

from pathlib import Path

from textwrap import dedent

from streamlit_option_menu import option_menu





st.set_page_config(

    page_title="NHL Analytics Hub",

    page_icon="🏒",

    layout="wide",

    initial_sidebar_state="expanded",

)





# ============================================================

# CSS

# ============================================================



st.markdown(

    dedent("""

    <style>

    #MainMenu { visibility: hidden; }

    footer { visibility: hidden; }



    .stApp,

    [data-testid="stAppViewContainer"] {

        background: #ffffff;

    }



    .block-container {

        max-width: 1180px;

        padding: 28px 42px 35px 42px;

    }



    section[data-testid="stSidebar"] {

        background: #eef0f4 !important;

        min-width: 260px !important;

        max-width: 260px !important;

    }



    section[data-testid="stSidebar"] > div {

        background: #eef0f4 !important;

        padding: 20px 18px 18px 18px;

    }



    .sidebar-card {

        background: #ffffff;

        border-radius: 7px;

        padding: 20px 12px 10px 12px;

        margin-top: 54px;

    }



    .sidebar-brand {

        display: flex;

        align-items: flex-start;

        gap: 10px;

        padding: 0 9px 13px 9px;

        border-bottom: 1px solid #d8d8d8;

        color: #303746;

        font-family: Arial, sans-serif;

        font-size: 20px;

        line-height: 1.45;

    }



    .sidebar-brand-icon {

        font-size: 20px;

        color: #24324a;

    }



    div[data-testid="stSidebar"] .nav-link {

        border-radius: 5px !important;

        margin: 3px 0 !important;

        padding: 10px 10px !important;

        font-family: Arial, sans-serif !important;

        font-size: 16px !important;

        color: #344054 !important;

    }



    div[data-testid="stSidebar"] .nav-link:hover {

        background: #f5f5f5 !important;

        color: #344054 !important;

    }



    div[data-testid="stSidebar"] .nav-link-selected {

        background: #ff5050 !important;

        color: #ffffff !important;

        font-weight: 700 !important;

    }



    div[data-testid="stSidebar"] .nav-link-selected span,

    div[data-testid="stSidebar"] .nav-link-selected i {

        color: #ffffff !important;

    }



    .dashboard-shell {

        border-top: 1px solid #ff5050;

        border-radius: 5px 5px 0 0;

        padding-top: 0;

    }



    .hero {

        display: flex;

        align-items: flex-start;

        min-height: 205px;

        padding-top: 5px;

    }



    .hero-image-wrap {

        width: 205px;

        min-width: 205px;

        height: 185px;

        display: flex;

        align-items: center;

        justify-content: center;

    }



    .hero-image {

        width: 180px;

        height: auto;

        object-fit: contain;

    }



    .hero-content {

        flex: 1;

        padding-left: 8px;

        padding-top: 16px;

    }



    .hero-title {

        color: #30333f;

        font-family: Arial, sans-serif;

        font-size: 39px;

        font-weight: 800;

        line-height: 1.1;

        margin: 5px 0 42px 0;

        letter-spacing: -1px;

    }



    .hero-title-icon {

        font-size: 35px;

        margin-right: 7px;

    }



    .hero-line {

        height: 1px;

        background: #d9d9d9;

        width: 100%;

    }



    .subtitle {

        color: #394150;

        font-family: Arial, sans-serif;

        font-size: 15px;

        margin: 0 0 20px 0;

    }



    .kpi-row {

        display: grid;

        grid-template-columns: repeat(4, 1fr);

        gap: 13px;

        margin-bottom: 45px;

    }



    .kpi-card {

        border: 1px solid #dedede;

        border-radius: 7px;

        background: #ffffff;

        min-height: 102px;

        padding: 13px 14px 12px 14px;

        box-sizing: border-box;

    }



    .kpi-label {

        color: #343a46;

        font-family: Arial, sans-serif;

        font-size: 13px;

        margin-bottom: 7px;

    }



    .kpi-value {

        color: #303746;

        font-family: Arial, sans-serif;

        font-size: 32px;

        font-weight: 400;

        line-height: 1;

    }



    .divider {

        height: 1px;

        background: #dedede;

        margin: 0 0 30px 0;

    }



    .highlight-row {

        display: grid;

        grid-template-columns: repeat(3, 1fr);

        gap: 13px;

        margin-bottom: 47px;

    }



    .highlight-card {

        border: 1px solid #dedede;

        border-radius: 7px;

        background: #ffffff;

        min-height: 118px;

        padding: 14px 14px 11px 14px;

        box-sizing: border-box;

    }



    .highlight-label {

        color: #343a46;

        font-family: Arial, sans-serif;

        font-size: 13px;

        margin-bottom: 5px;

    }



    .highlight-value {

        color: #303746;

        font-family: Arial, sans-serif;

        font-size: 29px;

        font-weight: 400;

        line-height: 1.15;

        white-space: nowrap;

        overflow: hidden;

        text-overflow: ellipsis;

    }



    .highlight-delta {

        color: #10a95a;

        font-family: Arial, sans-serif;

        font-size: 13px;

        margin-top: 5px;

    }

    </style>

    """),

    unsafe_allow_html=True,

)





# ============================================================

# DATABASE

# ============================================================



@st.cache_resource

def get_db_connection():

    return mysql.connector.connect(

        host="localhost",

        user="root",

        password = os.getenv("NHL_DB_PASSWORD"),

        database="nhl_analytics",

    )





def run_query(query, params=None):

    try:

        conn = get_db_connection()



        if not conn.is_connected():

            conn.reconnect(attempts=1, delay=0)



        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, params or ())

        rows = cursor.fetchall()

        cursor.close()



        return pd.DataFrame(rows)



    except Exception as error:

        st.error(f"Database error: {error}")

        return pd.DataFrame()





def table_exists(table_name):

    result = run_query(

        """

        SELECT COUNT(*) AS table_count

        FROM information_schema.tables

        WHERE table_schema = DATABASE()

          AND table_name = %s

        """,

        (table_name,),

    )



    return (

        not result.empty

        and int(result.iloc[0]["table_count"]) > 0

    )





# ============================================================

# SIDEBAR

# ============================================================



with st.sidebar:



    st.markdown(

        dedent("""

        <div class="sidebar-card">

            <div class="sidebar-brand">

                <span class="sidebar-brand-icon">▱</span>

                <span>NHL Analytics<br>Hub</span>

            </div>

        </div>

        """),

        unsafe_allow_html=True,

    )



    selected_page = option_menu(

        menu_title=None,

        options=[

            "Home",

            "Standings",

            "Team Info",

            "Player Search",

            "Game Results",

            "Leaderboards",

            "SQL Query",

        ],

        icons=[

            "house",

            "list-ul",

            "people",

            "search",

            "controller",

            "bar-chart",

            "code-slash",

        ],

        default_index=0,

        styles={

            "container": {

                "padding": "0 !important",

                "background-color": "#ffffff",

                "border-radius": "0 0 7px 7px",

            },

            "icon": {

                "font-size": "14px",

            },

            "nav-link": {

                "font-size": "16px",

                "text-align": "left",

                "margin": "3px 0",

                "--hover-color": "#f5f5f5",

            },

            "nav-link-selected": {

                "background-color": "#ff5050",

                "font-weight": "700",

            },

        },

    )





# ============================================================

# HOME

# ============================================================



if selected_page == "Home":



    teams_df = run_query("SELECT COUNT(*) AS total FROM teams")

    games_df = run_query("SELECT COUNT(*) AS total FROM games")



    goals_df = run_query(

        """

        SELECT COALESCE(SUM(goals_for), 0) AS total

        FROM standings

        """

    )



    total_teams = int(teams_df.iloc[0]["total"]) if not teams_df.empty else 32

    total_games = int(games_df.iloc[0]["total"]) if not games_df.empty else 1498

    total_goals = float(goals_df.iloc[0]["total"]) if not goals_df.empty else 8205.0



    total_players = 795

    top_scorer = "Connor McDavid"

    top_scorer_points = 138

    best_goalie = "Dylan Garand"

    best_save_pct = 0.947917

    league_leader = "Colorado Avalanche"

    league_points = 121



    if table_exists("players"):

        player_count = run_query(

            "SELECT COUNT(*) AS total FROM players"

        )

        if not player_count.empty:

            total_players = int(player_count.iloc[0]["total"])



    if table_exists("skater_season_stats"):

        scorer = run_query(

            """

            SELECT

                p.player_name AS player_name,

                s.points

            FROM skater_season_stats s

            JOIN players p ON p.player_id = s.player_id

            ORDER BY s.points DESC

            LIMIT 1

            """

        )



        if not scorer.empty:

            top_scorer = scorer.iloc[0]["player_name"]

            top_scorer_points = int(scorer.iloc[0]["points"])



    if table_exists("goalie_season_stats"):

        goalie = run_query(

            """

            SELECT

                p.player_name AS player_name,

                g.save_pct

            FROM goalie_season_stats g

            JOIN players p ON p.player_id = g.player_id

            WHERE g.games_played > 0

            ORDER BY g.save_pct DESC

            LIMIT 1

            """

        )



        if not goalie.empty:

            best_goalie = goalie.iloc[0]["player_name"]

            best_save_pct = float(goalie.iloc[0]["save_pct"])



    league = run_query(

        """

        SELECT

            t.team_name,

            s.points

        FROM standings s

        JOIN teams t ON t.team_id = s.team_id

        ORDER BY s.points DESC

        LIMIT 1

        """

    )



    if not league.empty:

        league_leader = league.iloc[0]["team_name"]

        league_points = int(league.iloc[0]["points"])





    # ONE COMPLETE HTML BLOCK.

    # This is the key fix for the HTML appearing as code.



        home_html = """

        <div class="dashboard-shell">



            <div class="hero">



                <div class="hero-image-wrap">

                    <img

                        class="hero-image"

                        src="data:image/png;base64,IMAGE_DATA"

                        alt="NHL hockey players"

                    />

                </div>



                <div class="hero-content">



                    <div class="hero-title">

                        <span class="hero-title-icon">🏒</span>

                        NHL Analytics Hub

                    </div>



                    <div class="hero-line"></div>



                </div>



            </div>



            <div class="subtitle">

                API-driven hockey data pipeline with SQL analysis and Streamlit dashboard

            </div>



            <div class="kpi-row">



                <div class="kpi-card">

                    <div class="kpi-label">🏒 Total Teams</div>

                    <div class="kpi-value">TOTAL_TEAMS</div>

                </div>



                <div class="kpi-card">

                    <div class="kpi-label">🧍 Total Players</div>

                    <div class="kpi-value">TOTAL_PLAYERS</div>

                </div>



                <div class="kpi-card">

                    <div class="kpi-label">🎮 Total Games</div>

                    <div class="kpi-value">TOTAL_GAMES</div>

                </div>



                <div class="kpi-card">

                    <div class="kpi-label">🥅 Total Goals Scored</div>

                    <div class="kpi-value">TOTAL_GOALS</div>

                </div>



            </div>



            <div class="divider"></div>



            <div class="highlight-row">



                <div class="highlight-card">

                    <div class="highlight-label">⭐ Top Scorer</div>

                    <div class="highlight-value">TOP_SCORER</div>

                    <div class="highlight-delta">↑ TOP_SCORER_POINTS pts</div>

                </div>



                <div class="highlight-card">

                    <div class="highlight-label">💎 Best Save %</div>

                    <div class="highlight-value">BEST_GOALIE</div>

                    <div class="highlight-delta">↑ BEST_SAVE_PCT</div>

                </div>



                <div class="highlight-card">

                    <div class="highlight-label">🏆 League Leader</div>

                    <div class="highlight-value">LEAGUE_LEADER</div>

                    <div class="highlight-delta">↑ LEAGUE_POINTS pts</div>

                </div>



            </div>



            <div class="divider"></div>



        </div>

        """
    home_html = home_html.replace("TOTAL_TEAMS", f"{total_teams:,}")

    home_html = home_html.replace("TOTAL_PLAYERS", f"{total_players:,}")

    home_html = home_html.replace("TOTAL_GAMES", f"{total_games:,}")

    home_html = home_html.replace("TOTAL_GOALS", f"{total_goals:,.1f}")

    home_html = home_html.replace("TOP_SCORER_POINTS", str(top_scorer_points))

    home_html = home_html.replace("TOP_SCORER", top_scorer)

    home_html = home_html.replace("BEST_GOALIE", best_goalie)

    home_html = home_html.replace("BEST_SAVE_PCT", f"{best_save_pct:.6f}")

    home_html = home_html.replace("LEAGUE_LEADER", league_leader)

    home_html = home_html.replace("LEAGUE_POINTS", str(league_points))



    st.markdown(
        dedent(home_html),

        unsafe_allow_html=True,

    )





# ============================================================

# STANDINGS

# ============================================================



elif selected_page == "Standings":



    st.title("Standings")



    df = run_query(

            """

            SELECT

                t.team_abbrev AS Team,

                t.team_name AS Team_Name,

                t.conference_name AS Conference,

                t.division_name AS Division,

                s.games_played AS GP,

                s.wins AS W,

                s.losses AS L,

                s.ot_losses AS OT,

                s.points AS PTS,

                s.goals_for AS GF,

                s.goals_against AS GA

            FROM standings s

            JOIN teams t ON t.team_id = s.team_id

            ORDER BY s.points DESC, s.wins DESC

            """

        )



    st.dataframe(df, use_container_width=True, hide_index=True)





# ============================================================

# TEAM INFO

# ============================================================



elif selected_page == "Team Info":



    st.title("Team Info")



    teams = run_query(

        """

        SELECT

            team_id,

            team_name,

            team_abbrev,

            conference_name,

            division_name

        FROM teams

        ORDER BY team_name

        """

    )



    if not teams.empty:



        team_name = st.selectbox(

            "Select Team",

            teams["team_name"].tolist(),

        )



        team = teams[teams["team_name"] == team_name].iloc[0]



        st.write(

            f"**{team['team_name']}** — "

            f"{team['conference_name']} / "

            f"{team['division_name']}"

        )





# ============================================================

# PLAYER SEARCH

# ============================================================



elif selected_page == "Player Search":



    st.title("Player Search")



    if not table_exists("players"):



        st.info("Players table is not loaded yet.")



    else:



        search = st.text_input("Search Player")



        if search:



            df = run_query(

                """

                SELECT

                    CONCAT(first_name, ' ', last_name) AS Player,

                    position AS Position,

                    jersey_number AS Jersey

                FROM players

                WHERE first_name LIKE %s

                   OR last_name LIKE %s

                ORDER BY last_name

                """,

                (f"%{search}%", f"%{search}%"),

            )



            st.dataframe(df, use_container_width=True, hide_index=True)





# ============================================================

# GAME RESULTS

# ============================================================



elif selected_page == "Game Results":



    st.title("Game Results")



    df = run_query(

        """

        SELECT

            g.game_id,

            g.game_date,

            ht.team_abbrev AS Home,

            at.team_abbrev AS Away,

            g.home_score AS Home_Score,

            g.away_score AS Away_Score,

            g.game_state AS Game_State,

            g.venue_name AS Venue

        FROM games g

        JOIN teams ht ON ht.team_id = g.home_team_id

        JOIN teams at ON at.team_id = g.away_team_id

        ORDER BY g.game_date DESC

        LIMIT 500

        """

    )



    st.dataframe(df, use_container_width=True, hide_index=True)





# ============================================================

# LEADERBOARDS

# ============================================================



elif selected_page == "Leaderboards":



    st.title("Leaderboards")



    col1, col2 = st.columns(2)



    with col1:



        st.subheader("Most Wins")



        df = run_query(

            """

            SELECT

                t.team_name AS Team,

                s.wins AS Wins

            FROM standings s

            JOIN teams t ON t.team_id = s.team_id

            ORDER BY s.wins DESC

            LIMIT 10

            """

        )



        st.dataframe(df, use_container_width=True, hide_index=True)



    with col2:



        st.subheader("Most Goals")



        df = run_query(

            """

            SELECT

                t.team_name AS Team,

                s.goals_for AS Goals

            FROM standings s

            JOIN teams t ON t.team_id = s.team_id

            ORDER BY s.goals_for DESC

            LIMIT 10

            """

        )



        st.dataframe(df, use_container_width=True, hide_index=True)





# ============================================================

# SQL QUERY

# ============================================================



elif selected_page == "SQL Query":



    st.title("SQL Query")



    query_options = {

        "Teams with Most Wins": """

            SELECT

                t.team_name,

                s.wins

            FROM standings s

            JOIN teams t ON t.team_id = s.team_id

            ORDER BY s.wins DESC

            LIMIT 10;

        """,



        "Teams with Most Goals": """

            SELECT

                t.team_name,

                s.goals_for

            FROM standings s

            JOIN teams t ON t.team_id = s.team_id

            ORDER BY s.goals_for DESC

            LIMIT 10;

        """,



        "Average Goals per Game": """

            SELECT

                ROUND(AVG(home_score + away_score), 2)

                AS average_goals

            FROM games

            WHERE game_state = 'OFF';

        """,



        "Close Games": """

            SELECT

                COUNT(*) AS close_games

            FROM games

            WHERE ABS(home_score - away_score) <= 1

              AND game_state = 'OFF';

        """,

    }



    selected_query = st.selectbox(

        "Select Query",

        list(query_options.keys()),

    )



    st.code(query_options[selected_query], language="sql")



    if st.button("Run Query"):



        result = run_query(query_options[selected_query])



        st.dataframe(

            result,

            use_container_width=True,

            hide_index=True,

        )
