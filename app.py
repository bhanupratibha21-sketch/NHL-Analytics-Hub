import os
from pathlib import Path
import mysql.connector
import pandas as pd
import streamlit as st

from dotenv import load_dotenv

load_dotenv()

from streamlit_option_menu import option_menu

st.set_page_config(page_title="NHL Analytics Hub", page_icon="🏒", layout="wide")

@st.cache_resource
@st.cache_resource
@st.cache_resource
def get_db_connection():
    password = os.getenv("NHL_DB_PASSWORD")

    if not password:
        raise RuntimeError(
            "NHL_DB_PASSWORD environment variable is not configured."
        )

    return mysql.connector.connect(
        host=os.getenv("NHL_DB_HOST", "localhost"),
        user=os.getenv("NHL_DB_USER", "root"),
        password=password,
        database=os.getenv("NHL_DB_NAME", "nhl_analytics"),
    )

def run_query(query, params=None):
    try:
        conn = get_db_connection()

        if not conn.is_connected():
            conn.reconnect(attempts=1, delay=0)

        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(query, params or ())
            rows = cursor.fetchall()
            columns = cursor.column_names
        finally:
            cursor.close()

        return pd.DataFrame(rows, columns=columns)

    except Exception as error:
        st.error(f"Database error: {error}")
        return pd.DataFrame()

# ============================================================
# GLOBAL STYLING
# ============================================================

# ============================================================
# NHL DASHBOARD STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       MAIN APP
       ===================================================== */

    .stApp {
        background-color: #f5f6f8;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 25px;
        padding-bottom: 45px;
        padding-left: 35px;
        padding-right: 35px;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background-color: #f58220;
        border-right: none;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 20px;
    }

    /* Sidebar text */

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }


    /* =====================================================
       SIDEBAR NAVIGATION
       ===================================================== */

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label {

        background-color: transparent;

        padding: 10px 12px;

        margin-bottom: 5px;

        border-radius: 8px;

        font-weight: 500;

        transition: 0.2s;
    }


    /* Navigation hover */

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label:hover {

        background-color: rgba(
            255,
            255,
            255,
            0.20
        );
    }


    /* =====================================================
       PAGE TITLES
       ===================================================== */

    h1 {
        color: #102a43;
        font-size: 34px;
        font-weight: 700;
    }

    h2 {
        color: #102a43;
        font-weight: 650;
    }

    h3 {
        color: #243b53;
        font-weight: 600;
    }


    /* =====================================================
       KPI / METRIC CARDS
       ===================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {

        background-color: #ffffff;

        border-radius: 12px;

        border: 1px solid #e4e7eb;

        box-shadow:
            0 2px 8px
            rgba(0, 0, 0, 0.05);

        transition: 0.2s;
    }


    /* Card hover */

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {

        box-shadow:
            0 5px 15px
            rgba(0, 0, 0, 0.08);

        transform: translateY(-1px);
    }


    /* Metric value */

    div[data-testid="stMetricValue"] {

        color: #102a43;

        font-size: 30px;

        font-weight: 700;
    }


    /* Metric label */

    div[data-testid="stMetricLabel"] {

        color: #627d98;

        font-size: 14px;

        font-weight: 600;
    }


    /* =====================================================
       DATA TABLES
       ===================================================== */

    div[data-testid="stDataFrame"] {

        background-color: #ffffff;

        border: 1px solid #e4e7eb;

        border-radius: 10px;

        overflow: hidden;

        box-shadow:
            0 2px 6px
            rgba(0, 0, 0, 0.04);
    }


    /* =====================================================
       BUTTON
       ===================================================== */

    .stButton > button {

        background-color: #f58220;

        color: #ffffff;

        border: none;

        border-radius: 8px;

        font-weight: 600;

        padding: 8px 20px;
    }


    .stButton > button:hover {

        background-color: #dc6f13;

        color: #ffffff;

        border: none;
    }


    /* =====================================================
       DOWNLOAD BUTTON
       ===================================================== */

    .stDownloadButton > button {

        background-color: #102a43;

        color: white;

        border-radius: 8px;

        border: none;

        font-weight: 600;
    }


    /* =====================================================
       INPUTS / SELECT BOX
       ===================================================== */

    div[data-baseweb="select"] > div {

        background-color: #ffffff;

        border-radius: 8px;
    }


    div[data-baseweb="input"] > div {

        background-color: #ffffff;

        border-radius: 8px;
    }


    textarea {

        border-radius: 8px !important;
    }


    /* =====================================================
       DIVIDERS
       ===================================================== */

    hr {

        border-color: #e4e7eb;

        margin-top: 22px;

        margin-bottom: 22px;
    }


    /* =====================================================
       CAPTION
       ===================================================== */

    .stCaption {

        color: #829ab1;
    }


    /* =====================================================
       REMOVE STREAMLIT DECORATION
       ===================================================== */

    [data-testid="stHeader"] {

        background-color:
            rgba(0,0,0,0);
    }


    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## 🏒 NHL Analytics Hub")
    st.divider()

    page = option_menu(
        menu_title=None,
        options=[
            "🏠 Home",
            "📊 Standings",
            "🏒 Team Info",
            "🔎 Player Search",
            "🎮 Game Results",
            "🏆 Leaderboards",
            "💻 SQL Query",
        ],
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#f58220",
            },
            "nav-link": {
                "font-size": "15px",
                "color": "white",
                "padding": "12px",
                "margin": "4px 0",
                "border-radius": "8px",
            },
            "nav-link-hover": {
                "background-color": "#dc6f13",
            },
            "nav-link-selected": {
                "background-color": "#ffffff",
                "color": "#102a43",
                "font-weight": "600",
            },
        },
    )
def show_home():

    # --------------------------------------------------------
    # BASIC COUNTS
    # --------------------------------------------------------

    teams_df = run_query("SELECT COUNT(*) AS total FROM teams")
    players_df = run_query("SELECT COUNT(*) AS total FROM players")
    games_df = run_query("SELECT COUNT(*) AS total FROM games")

    goals_df = run_query("""
        SELECT COALESCE(SUM(goals_for), 0) AS total
        FROM standings
    """)

    total_teams = int(teams_df.iloc[0]["total"]) if not teams_df.empty else 0
    total_players = int(players_df.iloc[0]["total"]) if not players_df.empty else 0
    total_games = int(games_df.iloc[0]["total"]) if not games_df.empty else 0
    total_goals = int(goals_df.iloc[0]["total"]) if not goals_df.empty else 0


    # --------------------------------------------------------
    # LEAGUE LEADER
    # --------------------------------------------------------

    leader_df = run_query("""
        SELECT
            t.team_name,
            s.points
        FROM standings s
        JOIN teams t
            ON t.team_id = s.team_id
        ORDER BY
            s.points DESC,
            s.wins DESC
        LIMIT 1
    """)

    if not leader_df.empty:
        league_leader = str(leader_df.iloc[0]["team_name"])
        league_points = int(leader_df.iloc[0]["points"])
    else:
        league_leader = "N/A"
        league_points = 0


    # --------------------------------------------------------
    # TOP SCORER
    # --------------------------------------------------------

    top_scorer_df = run_query("""
        SELECT
            p.player_name,
            s.points
        FROM skater_season_stats s
        JOIN players p
            ON s.player_id = p.nhl_player_id
        WHERE s.season = '20252026'
        ORDER BY s.points DESC
        LIMIT 1
    """)

    if not top_scorer_df.empty:
        top_scorer = str(
            top_scorer_df.iloc[0]["player_name"]
        )

        top_scorer_points = int(
            top_scorer_df.iloc[0]["points"]
        )

    else:
        top_scorer = "N/A"
        top_scorer_points = 0


    # --------------------------------------------------------
    # BEST GOALIE
    # Minimum 20 games prevents tiny samples
    # --------------------------------------------------------

    best_goalie_df = run_query("""
        SELECT
            p.player_name,
            g.save_pct
        FROM goalie_season_stats g
        JOIN players p
            ON g.player_id = p.nhl_player_id
        WHERE g.season = '20252026'
          AND g.games_played >= 20
        ORDER BY g.save_pct DESC
        LIMIT 1
    """)

    if not best_goalie_df.empty:
        best_goalie = str(
            best_goalie_df.iloc[0]["player_name"]
        )

        best_save_pct = float(
            best_goalie_df.iloc[0]["save_pct"]
        )

    else:
        best_goalie = "N/A"
        best_save_pct = 0


    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    image_path = (
        Path(__file__).parent
        / "assets"
        / "nhl_players.png"
    )

    image_col, title_col = st.columns(
        [1.2, 4.8],
        gap="medium",
    )

    with image_col:

        if image_path.exists():
            st.image(
                str(image_path),
                use_container_width=True,
            )

        else:
            st.info(
                "Add assets/nhl_players.png"
            )


    with title_col:

        st.title("🏒 NHL Analytics Hub")

        st.caption(
            "API-driven hockey data pipeline "
            "with SQL analysis and Streamlit dashboard"
        )


    st.divider()


    # --------------------------------------------------------
    # MAIN KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        with st.container(border=True):

            st.caption("🏒 Total Teams")

            st.metric(
                "Teams",
                f"{total_teams:,}",
                label_visibility="collapsed",
            )


    with col2:

        with st.container(border=True):

            st.caption("🧍 Total Players")

            st.metric(
                "Players",
                f"{total_players:,}",
                label_visibility="collapsed",
            )


    with col3:

        with st.container(border=True):

            st.caption("🎮 Total Games")

            st.metric(
                "Games",
                f"{total_games:,}",
                label_visibility="collapsed",
            )


    with col4:

        with st.container(border=True):

            st.caption("🥅 Total Goals")

            st.metric(
                "Goals",
                f"{total_goals:,}",
                label_visibility="collapsed",
            )


    st.divider()


    # --------------------------------------------------------
    # HIGHLIGHT CARDS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        with st.container(border=True):

            st.caption("⭐ Top Scorer")

            st.subheader(top_scorer)

            st.success(
                f"↑ {top_scorer_points} pts"
            )


    with col2:

        with st.container(border=True):

            st.caption("🥅 Best Save %")

            st.subheader(best_goalie)

            st.success(
                f"↑ {best_save_pct:.3f}"
            )


    with col3:

        with st.container(border=True):

            st.caption("🏆 League Leader")

            st.subheader(league_leader)

            st.success(
                f"↑ {league_points} pts"
            )

# ============================================================
# STANDINGS PAGE
# ============================================================

def show_standings():

    st.title("📊 NHL Standings")

    st.caption(
        "Current team standings by conference and division"
    )

    st.divider()

    # --------------------------------------------------------
    # LOAD STANDINGS DATA
    # --------------------------------------------------------

    standings_df = run_query(
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
        JOIN teams t
            ON t.team_id = s.team_id
        ORDER BY
            s.points DESC,
            s.wins DESC
        """
    )

    if standings_df.empty:
        st.warning("No standings data found.")
        return

    # --------------------------------------------------------
    # SUMMARY CARDS
    # --------------------------------------------------------

    leader = standings_df.iloc[0]["Team_Name"]
    highest_points = int(
        standings_df["PTS"].max()
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.caption("🏒 Total Teams")
            st.metric(
                "Teams",
                len(standings_df),
                label_visibility="collapsed",
            )

    with col2:
        with st.container(border=True):
            st.caption("🏆 League Leader")
            st.metric(
                "Leader",
                leader,
                label_visibility="collapsed",
            )

    with col3:
        with st.container(border=True):
            st.caption("⭐ Highest Points")
            st.metric(
                "Points",
                highest_points,
                label_visibility="collapsed",
            )

    st.divider()

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    search_team = st.text_input(
    "🔎 Search Team",
    placeholder="Enter team name or abbreviation..."
)

    filter_col1, filter_col2 = st.columns(2)

    conferences = sorted(
        standings_df["Conference"]
        .dropna()
        .unique()
        .tolist()
    )

    divisions = sorted(
        standings_df["Division"]
        .dropna()
        .unique()
        .tolist()
    )

    with filter_col1:

        selected_conference = st.selectbox(
            "Conference",
            ["All"] + conferences,
        )

    with filter_col2:

        selected_division = st.selectbox(
            "Division",
            ["All"] + divisions,
        )

    # --------------------------------------------------------
    # FILTER DATA
    # --------------------------------------------------------

    conditions = []
    params = []

    if search_team.strip():
        conditions.append(
            "(t.team_name LIKE %s OR t.team_abbrev LIKE %s)"
        )
        search_value = f"%{search_team.strip()}%"
        params.extend([search_value, search_value])

    if selected_conference != "All":
        conditions.append("t.conference_name = %s")
        params.append(selected_conference)

    if selected_division != "All":
        conditions.append("t.division_name = %s")
        params.append(selected_division)

    where_clause = (
        "WHERE " + " AND ".join(conditions)
        if conditions
        else ""
    )


# --------------------------------------------------------
# DYNAMIC SQL FILTERING
# --------------------------------------------------------

    query = f"""
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
        JOIN teams t
            ON t.team_id = s.team_id
        {where_clause}
        ORDER BY
            s.points DESC,
            s.wins DESC
    """

    filtered_df = run_query(query, tuple(params))

    if filtered_df.empty:
        st.warning("No standings found for the selected filters.")
    # --------------------------------------------------------
    # STANDINGS TABLE
    # --------------------------------------------------------

    st.subheader("Team Standings")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Team": "Team",
            "Team_Name": "Team Name",
            "Conference": "Conference",
            "Division": "Division",
            "GP": "GP",
            "W": "W",
            "L": "L",
            "OT": "OT",
            "PTS": "PTS",
            "GF": "GF",
            "GA": "GA",
        },
    )



# ============================================================
# TEAM INFO PAGE
# ============================================================

def show_team_info():

    st.title("🏒 Team Info")
    st.caption("Explore NHL team information and season performance")

    st.divider()

    # --------------------------------------------------------
    # LOAD TEAM DATA
    # --------------------------------------------------------

    teams_df = run_query(
        """
        SELECT
            t.team_id,
            t.team_name,
            t.team_abbrev,
            t.conference_name,
            t.division_name,
            s.games_played,
            s.wins,
            s.losses,
            s.ot_losses,
            s.points,
            s.goals_for,
            s.goals_against,
            s.home_wins,
            s.away_wins,
            s.streak_type,
            s.streak_count
        FROM teams t
        LEFT JOIN standings s
            ON t.team_id = s.team_id
        ORDER BY t.team_name
        """
    )

    if teams_df.empty:
        st.warning("No team data found.")
        return

    # --------------------------------------------------------
    # TEAM SELECTOR
    # --------------------------------------------------------

    selected_team = st.selectbox(
        "Select Team",
        teams_df["team_name"].tolist(),
    )

    team = teams_df[
        teams_df["team_name"] == selected_team
    ].iloc[0]

    st.divider()

    # --------------------------------------------------------
    # TEAM HEADER
    # --------------------------------------------------------

    st.subheader(
        f"{team['team_name']} ({team['team_abbrev']})"
    )

    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.write(
            f"**Conference:** "
            f"{team['conference_name']}"
        )

    with info_col2:
        st.write(
            f"**Division:** "
            f"{team['division_name']}"
        )

    st.divider()

    # --------------------------------------------------------
    # PRIMARY KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True):
            st.caption("🎮 Games Played")
            st.metric(
                "GP",
                int(team["games_played"]),
                label_visibility="collapsed",
            )

    with col2:
        with st.container(border=True):
            st.caption("✅ Wins")
            st.metric(
                "Wins",
                int(team["wins"]),
                label_visibility="collapsed",
            )

    with col3:
        with st.container(border=True):
            st.caption("❌ Losses")
            st.metric(
                "Losses",
                int(team["losses"]),
                label_visibility="collapsed",
            )

    with col4:
        with st.container(border=True):
            st.caption("⏱️ OT Losses")
            st.metric(
                "OT",
                int(team["ot_losses"]),
                label_visibility="collapsed",
            )

    # --------------------------------------------------------
    # SECOND KPI ROW
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.caption("⭐ Points")
            st.metric(
                "Points",
                int(team["points"]),
                label_visibility="collapsed",
            )

    with col2:
        with st.container(border=True):
            st.caption("🥅 Goals For")
            st.metric(
                "GF",
                int(team["goals_for"]),
                label_visibility="collapsed",
            )

    with col3:
        with st.container(border=True):
            st.caption("🛡️ Goals Against")
            st.metric(
                "GA",
                int(team["goals_against"]),
                label_visibility="collapsed",
            )

    st.divider()

    # --------------------------------------------------------
    # HOME / AWAY PERFORMANCE
    # --------------------------------------------------------

    st.subheader("🏠 Home vs ✈️ Away Performance")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.caption("🏠 Home Wins")
            st.metric(
                "Home Wins",
                int(team["home_wins"]),
                label_visibility="collapsed",
            )

    with col2:
        with st.container(border=True):
            st.caption("✈️ Away Wins")
            st.metric(
                "Away Wins",
                int(team["away_wins"]),
                label_visibility="collapsed",
            )

    # --------------------------------------------------------
    # STREAK
    # --------------------------------------------------------

    st.subheader("🔥 Current Streak")

    streak_type = team["streak_type"]
    streak_count = int(team["streak_count"])

    if streak_type == "W":
        st.success(
            f"Winning Streak: {streak_count} games"
        )

    elif streak_type == "L":
        st.error(
            f"Losing Streak: {streak_count} games"
        )

    else:
        st.info(
            f"Streak: {streak_type}{streak_count}"
        )
    # --------------------------------------------------------
    # TEAM ROSTER
    # --------------------------------------------------------

    st.divider()
    st.subheader("👥 Team Roster")

    roster_df = run_query(f"""
        SELECT
            p.player_name,
            p.position,
            p.jersey_number,
            p.nationality
        FROM players p
        WHERE p.team_id = {int(team['team_id'])}
        ORDER BY
            p.position,
            p.player_name
    """)

    if roster_df.empty:
        st.warning("No roster data found for this team.")

    else:
        st.write(f"**Total Players:** {len(roster_df)}")

        forwards = roster_df[
            roster_df["position"].isin(["C", "LW", "RW", "F"])
        ]

        defensemen = roster_df[
            roster_df["position"] == "D"
        ]

        goalies = roster_df[
            roster_df["position"] == "G"
        ]

        tab1, tab2, tab3 = st.tabs(
            [
                f"🏒 Forwards ({len(forwards)})",
                f"🛡️ Defensemen ({len(defensemen)})",
                f"🥅 Goalies ({len(goalies)})",
            ]
        )

        with tab1:
            if forwards.empty:
                st.info("No forwards found.")
            else:
                st.dataframe(
                    forwards.rename(
                        columns={
                            "player_name": "Player",
                            "position": "Position",
                            "jersey_number": "Jersey #",
                            "nationality": "Nationality",
                        }
                    ),
                    use_container_width=True,
                    hide_index=True,
                )

        with tab2:
            if defensemen.empty:
                st.info("No defensemen found.")
            else:
                st.dataframe(
                    defensemen.rename(
                        columns={
                            "player_name": "Player",
                            "position": "Position",
                            "jersey_number": "Jersey #",
                            "nationality": "Nationality",
                        }
                    ),
                    use_container_width=True,
                    hide_index=True,
                )

        with tab3:
            if goalies.empty:
                st.info("No goalies found.")
            else:
                st.dataframe(
                    goalies.rename(
                        columns={
                            "player_name": "Player",
                            "position": "Position",
                            "jersey_number": "Jersey #",
                            "nationality": "Nationality",
                        }
                    ),
                    use_container_width=True,
                    hide_index=True,
                )

# ============================================================
# PLAYER SEARCH PAGE
# ============================================================

def show_player_search():

    st.title("🔎 Player Search")
    st.caption("Search NHL players and view player information")

    st.divider()

    # --------------------------------------------------------
    # LOAD PLAYER DATA
    # --------------------------------------------------------

    players_df = run_query(
        """
        SELECT
            p.player_id,
            p.player_name,
            p.position,
            p.jersey_number,
            p.nationality,
            t.team_name,
            t.team_abbrev
        FROM players p
        LEFT JOIN teams t
            ON p.team_id = t.team_id
        ORDER BY p.player_name
        """
    )

    if players_df.empty:
        st.warning("No player data found.")
        return

    # --------------------------------------------------------
    # SEARCH BOX
    # --------------------------------------------------------

    search_text = st.text_input(
        "Search Player",
        placeholder="Enter player name...",
    )

    # --------------------------------------------------------
    # TEAM FILTER
    # --------------------------------------------------------

    teams = sorted(
        players_df["team_name"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_team = st.selectbox(
        "Filter by Team",
        ["All"] + teams,
    )


# --------------------------------------------------------
# DYNAMIC SQL FILTERING
# --------------------------------------------------------

    conditions = []
    params = []

    if search_text.strip():
        conditions.append("p.player_name LIKE %s")
        params.append(f"%{search_text.strip()}%")

    if selected_team != "All":
        conditions.append("t.team_name = %s")
        params.append(selected_team)

    where_clause = (
        "WHERE " + " AND ".join(conditions)
        if conditions
        else ""
    )

    query = f"""
        SELECT
            p.player_id,
            p.player_name,
            p.position,
            p.jersey_number,
            p.nationality,
            t.team_name,
            t.team_abbrev
        FROM players p
        LEFT JOIN teams t
            ON p.team_id = t.team_id
        {where_clause}
        ORDER BY p.player_name
    """

    filtered_df = run_query(query, tuple(params))
    # --------------------------------------------------------
    # RESULT COUNT
    # --------------------------------------------------------

    st.write(
        f"**Players Found:** {len(filtered_df)}"
    )

    # --------------------------------------------------------
    # PLAYER TABLE
    # --------------------------------------------------------

    display_df = filtered_df[
        [
            "player_name",
            "team_name",
            "team_abbrev",
            "position",
            "jersey_number",
            "nationality",
        ]
    ].copy()

    display_df.columns = [
        "Player",
        "Team",
        "Team Code",
        "Position",
        "Jersey #",
        "Nationality",
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    # --------------------------------------------------------
    # PLAYER DETAILS
    # --------------------------------------------------------

    if not filtered_df.empty:

        st.divider()
        st.subheader("👤 Player Details")

        selected_player = st.selectbox(
            "Select Player",
            filtered_df["player_name"]
            .tolist(),
        )

        player = filtered_df[
            filtered_df["player_name"]
            == selected_player
        ].iloc[0]

        st.subheader(player["player_name"])

        st.caption(
            f"{player['team_name']} "
            f"({player['team_abbrev']})"
        )

        # ----------------------------------------------------
        # PLAYER KPI CARDS
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.caption("🏒 Position")

                position = (
                    player["position"]
                    if pd.notna(player["position"])
                    else "N/A"
                )

                st.metric(
                    "Position",
                    position,
                    label_visibility="collapsed",
                )

        with col2:
            with st.container(border=True):
                st.caption("👕 Jersey Number")

                jersey = (
                    int(player["jersey_number"])
                    if pd.notna(player["jersey_number"])
                    else "N/A"
                )

                st.metric(
                    "Jersey",
                    jersey,
                    label_visibility="collapsed",
                )

        with col3:
            with st.container(border=True):
                st.caption("🌍 Nationality")

                nationality = (
                    player["nationality"]
                    if pd.notna(player["nationality"])
                    else "N/A"
                )

                st.metric(
                    "Nationality",
                    nationality,
                    label_visibility="collapsed",
                )


# ============================================================
# GAME RESULTS PAGE
# ============================================================

def show_game_results():

    st.title("🎮 Game Results")
    st.caption(
        "Explore NHL game results by date, team and game state"
    )

    st.divider()

    # --------------------------------------------------------
    # LOAD GAME DATA
    # --------------------------------------------------------

    games_df = run_query(
        """
        SELECT
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
        FROM games
        ORDER BY game_date DESC
        """
    )

    if games_df.empty:
        st.warning("No game data found.")
        return

    # Convert date column
    games_df["game_date"] = pd.to_datetime(
        games_df["game_date"]
    )

    # --------------------------------------------------------
    # SUMMARY CARDS
    # --------------------------------------------------------

    total_games = len(games_df)

    completed_games = len(
        games_df[
            games_df["game_state"].isin(
                ["FINAL", "OFF"]
            )
        ]
    )

    total_goals = (
        games_df["home_score"].fillna(0).sum()
        + games_df["away_score"].fillna(0).sum()
    )

    avg_goals = (
        total_goals / total_games
        if total_games > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True):
            st.caption("🎮 Total Games")
            st.metric(
                "Games",
                f"{total_games:,}",
                label_visibility="collapsed",
            )

    with col2:
        with st.container(border=True):
            st.caption("✅ Completed Games")
            st.metric(
                "Completed",
                f"{completed_games:,}",
                label_visibility="collapsed",
            )

    with col3:
        with st.container(border=True):
            st.caption("🥅 Total Goals")
            st.metric(
                "Goals",
                f"{int(total_goals):,}",
                label_visibility="collapsed",
            )

    with col4:
        with st.container(border=True):
            st.caption("📈 Avg Goals / Game")
            st.metric(
                "Average",
                f"{avg_goals:.2f}",
                label_visibility="collapsed",
            )

    st.divider()

    # --------------------------------------------------------
    # FILTER OPTIONS
    # --------------------------------------------------------

    teams = sorted(
        set(
            games_df["home_team_abbrev"]
            .dropna()
            .tolist()
            +
            games_df["away_team_abbrev"]
            .dropna()
            .tolist()
        )
    )

    game_states = sorted(
        games_df["game_state"]
        .dropna()
        .unique()
        .tolist()
    )

    # --------------------------------------------------------
    # FILTER ROW 1
    # --------------------------------------------------------

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        selected_team = st.selectbox(
            "Team",
            ["All"] + teams,
        )

    with filter_col2:
        selected_state = st.selectbox(
            "Game State",
            ["All"] + game_states,
        )

    # --------------------------------------------------------
    # DATE FILTER
    # --------------------------------------------------------

    min_date = games_df["game_date"].min().date()
    max_date = games_df["game_date"].max().date()

    selected_dates = st.date_input(
        "Game Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )


# --------------------------------------------------------
# DYNAMIC SQL FILTERING
# --------------------------------------------------------

    conditions = []
    params = []

    # Team filter
    if selected_team != "All":
        conditions.append(
            "(home_team_abbrev = %s OR away_team_abbrev = %s)"
        )
        params.extend([selected_team, selected_team])

    # Game state filter
    if selected_state != "All":
        conditions.append("game_state = %s")
        params.append(selected_state)

    # Date range filter
    if len(selected_dates) == 2:
        conditions.append("game_date BETWEEN %s AND %s")
        params.extend([
            selected_dates[0],
            selected_dates[1],
        ])

    where_clause = (
        "WHERE " + " AND ".join(conditions)
        if conditions
        else ""
    )

    query = f"""
        SELECT
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
        FROM games
        {where_clause}
        ORDER BY game_date DESC
    """

    filtered_df = run_query(query, tuple(params))

    # Convert game_date even when DataFrame is empty
    filtered_df["game_date"] = pd.to_datetime(
        filtered_df["game_date"]
    )

    if filtered_df.empty:
        st.warning("No games found for the selected filters.")
    # --------------------------------------------------------
    # CREATE WINNER COLUMN
    # --------------------------------------------------------

    def get_winner(row):

        if pd.isna(row["home_score"]) or pd.isna(
            row["away_score"]
        ):
            return "N/A"

        if row["home_score"] > row["away_score"]:
            return row["home_team_abbrev"]

        elif row["away_score"] > row["home_score"]:
            return row["away_team_abbrev"]

        return "Tie"

    filtered_df = filtered_df.copy()

    filtered_df["Winner"] = filtered_df.apply(
        get_winner,
        axis=1,
    )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    st.divider()

    st.subheader("Game Results")

    st.write(
        f"**Games Found:** {len(filtered_df):,}"
    )

    # --------------------------------------------------------
    # DISPLAY TABLE
    # --------------------------------------------------------

    display_df = filtered_df[
        [
            "game_date",
            "away_team_abbrev",
            "away_score",
            "home_team_abbrev",
            "home_score",
            "Winner",
            "game_state",
            "venue_name",
        ]
    ].copy()

    display_df["game_date"] = (
        display_df["game_date"]
        .dt.strftime("%Y-%m-%d")
    )

    display_df.columns = [
        "Date",
        "Away Team",
        "Away Score",
        "Home Team",
        "Home Score",
        "Winner",
        "Status",
        "Venue",
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# LEADERBOARDS PAGE
# ============================================================

def show_leaderboards():

    st.title("🏆 NHL Leaderboards")
    st.caption(
        "Compare top NHL teams across wins, points, goals and performance"
    )

    st.divider()

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    leaderboard_df = run_query(
        """
        SELECT
            t.team_name,
            t.team_abbrev,
            t.conference_name,
            t.division_name,
            s.games_played,
            s.wins,
            s.losses,
            s.ot_losses,
            s.points,
            s.goals_for,
            s.goals_against,
            s.home_wins,
            s.away_wins
        FROM standings s
        JOIN teams t
            ON t.team_id = s.team_id
        """
    )

    if leaderboard_df.empty:
        st.warning("No leaderboard data found.")
        return

    # --------------------------------------------------------
    # LEADER CARDS
    # --------------------------------------------------------

    points_leader = leaderboard_df.loc[
        leaderboard_df["points"].idxmax()
    ]

    wins_leader = leaderboard_df.loc[
        leaderboard_df["wins"].idxmax()
    ]

    goals_leader = leaderboard_df.loc[
        leaderboard_df["goals_for"].idxmax()
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.caption("⭐ Points Leader")
            st.subheader(points_leader["team_name"])
            st.success(
                f"{int(points_leader['points'])} points"
            )

    with col2:
        with st.container(border=True):
            st.caption("🏆 Most Wins")
            st.subheader(wins_leader["team_name"])
            st.success(
                f"{int(wins_leader['wins'])} wins"
            )

    with col3:
        with st.container(border=True):
            st.caption("🥅 Most Goals")
            st.subheader(goals_leader["team_name"])
            st.success(
                f"{int(goals_leader['goals_for'])} goals"
            )

    st.divider()

    # --------------------------------------------------------
    # LEADERBOARD TYPE
    # --------------------------------------------------------

    leaderboard_type = st.selectbox(
        "Select Leaderboard",
        [
            "Points",
            "Wins",
            "Goals For",
            "Home Wins",
            "Away Wins",
            "Goal Difference",
        ],
    )

    # --------------------------------------------------------
    # CREATE GOAL DIFFERENCE
    # --------------------------------------------------------

    leaderboard_df["goal_difference"] = (
        leaderboard_df["goals_for"]
        - leaderboard_df["goals_against"]
    )

    metric_map = {
        "Points": "points",
        "Wins": "wins",
        "Goals For": "goals_for",
        "Home Wins": "home_wins",
        "Away Wins": "away_wins",
        "Goal Difference": "goal_difference",
    }

    selected_metric = metric_map[
        leaderboard_type
    ]

    # --------------------------------------------------------
    # TOP 10
    # --------------------------------------------------------

    top_10 = (
        leaderboard_df
        .sort_values(
            selected_metric,
            ascending=False,
        )
        .head(10)
        .copy()
    )

    st.subheader(
        f"Top 10 Teams — {leaderboard_type}"
    )

    # --------------------------------------------------------
    # BAR CHART
    # --------------------------------------------------------

    chart_df = (
        top_10[
            ["team_abbrev", selected_metric]
        ]
        .set_index("team_abbrev")
    )

    st.bar_chart(
        chart_df,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    display_df = top_10[
        [
            "team_abbrev",
            "team_name",
            "conference_name",
            "division_name",
            selected_metric,
        ]
    ].copy()

    display_df.insert(
        0,
        "Rank",
        range(1, len(display_df) + 1),
    )

    display_df.columns = [
        "Rank",
        "Team",
        "Team Name",
        "Conference",
        "Division",
        leaderboard_type,
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # --------------------------------------------------------
    # HOME VS AWAY WINS
    # --------------------------------------------------------

    st.subheader("🏠 Home vs ✈️ Away Wins")

    home_away_df = (
        leaderboard_df[
            [
                "team_abbrev",
                "home_wins",
                "away_wins",
            ]
        ]
        .set_index("team_abbrev")
    )

    st.bar_chart(
        home_away_df,
        use_container_width=True,
    )



# ============================================================
# SQL QUERY PAGE
# ============================================================

def show_sql_query():

    st.title("💻 SQL Query")
    st.caption(
        "Run read-only SQL queries against the NHL Analytics database"
    )

    st.divider()

    # --------------------------------------------------------
    # DATABASE INFORMATION
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True):
            st.caption("📋 Table")
            st.subheader("games")

    with col2:
        with st.container(border=True):
            st.caption("📋 Table")
            st.subheader("teams")

    with col3:
        with st.container(border=True):
            st.caption("📋 Table")
            st.subheader("standings")

    with col4:
        with st.container(border=True):
            st.caption("📋 Table")
            st.subheader("players")

    st.divider()

    # --------------------------------------------------------
    # SAMPLE QUERIES
    # --------------------------------------------------------

    st.subheader("📚 Sample Queries")

    sample_query = st.selectbox(
        "Choose a sample query",
        [
            "Custom Query",
            "Top 10 Teams by Points",
            "Top 10 Teams by Wins",
            "Top 10 Teams by Goals",
            "Home vs Away Wins",
            "Recent Games",
            "Players by Team",
            "Top 5 Point Scorers",
            "Players with 20+ Goals and 30+ Assists",
            "Teams Above League Average Points",
            "Divisions with Average Points Above 90",
            "Top Scorers per Team",
            "Best Save Percentage Goalies",
        ],
    )

    queries = {

        "Custom Query":
        """SELECT * FROM teams LIMIT 10;""",

        "Top 10 Teams by Points":
        """
SELECT
    t.team_name,
    t.team_abbrev,
    s.games_played,
    s.wins,
    s.losses,
    s.ot_losses,
    s.points
FROM standings s
JOIN teams t
    ON t.team_id = s.team_id
ORDER BY s.points DESC
LIMIT 10;
""",

        "Top 10 Teams by Wins":
        """
SELECT
    t.team_name,
    t.team_abbrev,
    s.wins,
    s.losses,
    s.points
FROM standings s
JOIN teams t
    ON t.team_id = s.team_id
ORDER BY s.wins DESC
LIMIT 10;
""",

        "Top 10 Teams by Goals":
        """
SELECT
    t.team_name,
    t.team_abbrev,
    s.goals_for,
    s.goals_against
FROM standings s
JOIN teams t
    ON t.team_id = s.team_id
ORDER BY s.goals_for DESC
LIMIT 10;
""",

        "Home vs Away Wins":
        """
SELECT
    t.team_name,
    t.team_abbrev,
    s.home_wins,
    s.away_wins,
    (s.home_wins + s.away_wins) AS total_wins
FROM standings s
JOIN teams t
    ON t.team_id = s.team_id
ORDER BY total_wins DESC;
""",

        "Recent Games":
        """
SELECT
    game_date,
    away_team_abbrev,
    away_score,
    home_team_abbrev,
    home_score,
    game_state,
    venue_name
FROM games
ORDER BY game_date DESC
LIMIT 20;
""",

        "Players by Team":
        """
SELECT
    t.team_name,
    p.player_name,
    p.position,
    p.jersey_number,
    p.nationality
FROM players p
JOIN teams t
    ON t.team_id = p.team_id
ORDER BY t.team_name, p.player_name
LIMIT 100;
""",
# Query 7: Top 5 Point Scorers
        "Top 5 Point Scorers":
        """
SELECT
    p.player_name,
    s.goals,
    s.assists,
    s.points
FROM skater_season_stats s
JOIN players p
    ON s.player_id = p.nhl_player_id
WHERE s.season = 20252026
ORDER BY s.points DESC
LIMIT 5;
""",

        # Query 8: Players with 20+ Goals and 30+ Assists
        "Players with 20+ Goals and 30+ Assists":
        """
SELECT
    p.player_name,
    s.goals,
    s.assists,
    s.points
FROM skater_season_stats s
JOIN players p
    ON s.player_id = p.nhl_player_id
WHERE s.season = 20252026
  AND s.goals > 20
  AND s.assists > 30
ORDER BY s.points DESC;
""",

# Query 9: Teams Above League Average Points
"Teams Above League Average Points":
"""
SELECT
    t.team_name,
    t.team_abbrev,
    s.points
FROM standings s
JOIN teams t
    ON s.team_id = t.team_id
WHERE s.points > (
    SELECT AVG(points)
    FROM standings
)
ORDER BY s.points DESC;
""",

# Query 10: Divisions with Average Points Above 90
"Divisions with Average Points Above 90":
"""
SELECT
    t.division_name,
    ROUND(AVG(s.points), 2) AS avg_points
FROM standings s
JOIN teams t
    ON s.team_id = t.team_id
GROUP BY t.division_name
HAVING AVG(s.points) > 90
ORDER BY avg_points DESC;
""",

# Query 11: Top Scorers per Team
"Top Scorers per Team":
"""
SELECT
    t.team_name,
    p.player_name,
    s.goals,
    s.assists,
    s.points
FROM skater_season_stats s
JOIN players p
    ON s.player_id = p.nhl_player_id
JOIN teams t
    ON p.team_id = t.team_id
WHERE s.season = 20252026
AND s.points = (
    SELECT MAX(s2.points)
    FROM skater_season_stats s2
    JOIN players p2
        ON s2.player_id = p2.nhl_player_id
    WHERE p2.team_id = p.team_id
      AND s2.season = 20252026
)
ORDER BY t.team_name, p.player_name;
""",

# Query 12: Best Save Percentage Goalies
"Best Save Percentage Goalies":
"""
SELECT
    p.player_name,
    g.games_played,
    g.save_pct
FROM goalie_season_stats g
JOIN players p
    ON g.player_id = p.nhl_player_id
WHERE g.season = 20252026
  AND g.games_played >= 10
  AND g.save_pct IS NOT NULL
ORDER BY g.save_pct DESC
LIMIT 10;
""",
    }

    # --------------------------------------------------------
    # SQL EDITOR
    # --------------------------------------------------------

    st.subheader("✍️ SQL Editor")

    sql_query = st.text_area(
        "Enter SQL Query",
        value=queries[sample_query],
        height=250,
    )

    # --------------------------------------------------------
    # EXECUTE BUTTON
    # --------------------------------------------------------

    if st.button(
        "▶ Run Query",
        type="primary",
        use_container_width=True,
    ):

        cleaned_query = sql_query.strip()

        if not cleaned_query:
            st.warning("Please enter a SQL query.")
            return

        # ----------------------------------------------------
        # READ-ONLY VALIDATION
        # ----------------------------------------------------

        normalized_query = cleaned_query.lower().strip()

        allowed_query = (
            normalized_query.startswith("select")
            or normalized_query.startswith("with")
        )

        blocked_keywords = [
            "insert ",
            "update ",
            "delete ",
            "drop ",
            "alter ",
            "truncate ",
            "create ",
            "replace ",
            "grant ",
            "revoke ",
        ]

        contains_blocked_keyword = any(
            keyword in normalized_query
            for keyword in blocked_keywords
        )

        if not allowed_query or contains_blocked_keyword:

            st.error(
                "Only read-only SELECT queries are allowed."
            )
            return

        # ----------------------------------------------------
        # RUN QUERY
        # ----------------------------------------------------

        try:

            result_df = run_query(cleaned_query)

            if result_df.empty:

                st.info(
                    "Query executed successfully, "
                    "but no rows were returned."
                )

            else:

                st.success(
                    f"Query executed successfully — "
                    f"{len(result_df):,} rows returned."
                )

                st.dataframe(
                    result_df,
                    use_container_width=True,
                    hide_index=True,
                )

                # --------------------------------------------
                # DOWNLOAD RESULT
                # --------------------------------------------

                csv_data = result_df.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    "⬇️ Download Results as CSV",
                    data=csv_data,
                    file_name="nhl_query_results.csv",
                    mime="text/csv",
                )

        except Exception as error:

            st.error(
                f"Query failed: {error}"
            )


# ============================================================
# PAGE ROUTER
# ============================================================

if page == "🏠 Home":
    show_home()

elif page == "📊 Standings":
    show_standings()

elif page == "🏒 Team Info":
    show_team_info()

elif page == "🔎 Player Search":
    show_player_search()

elif page == "🎮 Game Results":
    show_game_results()

elif page == "🏆 Leaderboards":
    show_leaderboards()

elif page == "💻 SQL Query":
    show_sql_query()
