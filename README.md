# NHL Analytics Hub

## Project Overview

NHL Analytics Hub is a Python-based data analytics application that collects, processes, stores, and analyzes National Hockey League (NHL) data. It uses Python, Pandas, MySQL, SQL, and Streamlit to explore team standings, player statistics, game results, and performance metrics through an interactive dashboard.

## Project Objectives

- Fetch and explore NHL data using APIs.
- Convert API responses into structured datasets.
- Clean and validate data using Python and Pandas.
- Store NHL data in a MySQL relational database.
- Perform SQL-based analysis of teams, players, games, and statistics.
- Build an interactive Streamlit dashboard for data exploration.

## Technologies Used

- **Programming:** Python
- **Data Analysis:** Pandas
- **Database:** MySQL
- **Database Connectivity:** mysql-connector-python
- **Dashboard:** Streamlit
- **Dashboard Navigation:** streamlit-option-menu
- **API Integration:** Python Requests
- **Development:** Jupyter Notebook

## Project Structure

```text
NHL Analytics Hub/
├── app.py
├── app_old.py
├── db.py
├── database_setup.py
├── create_tables.py
├── create_teams_table.py
├── load_teams.py
├── load_games.py
├── load_game_stats.py
├── load_skater_season_stats.py
├── load_goalie_season_stats.py
├── update_nhl_player_ids.py
├── update_team_abbrev.py
├── data/
│   ├── games_cleaned.csv
│   └── raw/
│       └── standings.csv
├── notebooks/
│   └── Day1_API_Exploration.ipynb
├── src/
│   ├── api_test.py
│   ├── db.py
│   ├── load_players.py
│   ├── load_standings.py
│   └── sql_queries.sql
├── assets/
│   └── nhl_players.png
└── README.md
```

## Database Design

The project uses a MySQL database named `nhl_analytics`. The database stores NHL team standings, player information, game results, and player performance statistics across seven core tables.

| Table | Purpose |
|---|---|
| `teams` | Team information and identifiers |
| `standings` | Team standings, wins, losses, points, and goal statistics |
| `players` | Player profiles and team associations |
| `games` | Game dates, participating teams, scores, and status |
| `game_stats` | Player statistics associated with individual games |
| `skater_season_stats` | Season-level statistics for skaters |
| `goalie_season_stats` | Season-level statistics for goalies |

Primary keys identify records, while foreign keys link related teams, players, games, and statistics where configured in the database schema.

## Data Exploration and Validation

The NHL standings dataset was explored using Python and Pandas.

Validation included:

- Checking dataset structure and column names.
- Inspecting data types and missing values.
- Identifying duplicate records and team names.
- Confirming the number of unique teams.
- Generating descriptive statistics.
- Ranking teams based on points and other performance metrics.

The standings dataset contains 32 unique NHL teams.

### Main Standings Columns

- `team`
- `wins`
- `losses`
- `ot_losses`
- `points`
- `goals_for`
- `goals_against`
- `games_played`

## Team Performance Analysis

The analysis covers:

- Top 10 teams by points and wins.
- Teams with the most goals scored.
- Teams with the fewest goals conceded.
- Win percentage and points per game.
- Goals scored and conceded per game.
- Goal difference.
- Bottom 10 teams by points.
- Overall team ranking.

### Derived Metrics

- `goal_difference`
- `win_percentage`
- `points_per_game`
- `goals_for_per_game`
- `goals_against_per_game`

## Streamlit Dashboard

The Streamlit application provides an interactive interface for exploring NHL data and running analytical queries.

The dashboard is intended to provide the following sections:

- **Home:** Project overview and key metrics.
- **Standings:** Team rankings and season standings.
- **Team Info:** Team-level details and statistics.
- **Player Search:** Search and explore player information.
- **Game Results:** Game scores and results.
- **Leaderboards:** Compare top-performing teams and players.
- **SQL Query:** Explore analytical results using SQL queries.

Available sections and filters depend on the current implementation in `app.py`.

## SQL Analysis

SQL is used to retrieve and analyze data from the MySQL database. Analytical queries can cover:

- Team standings and rankings.
- Player performance.
- Game results and scores.
- Skater and goalie season statistics.
- Aggregations, filtering, sorting, and joins across related tables.

The SQL query collection is maintained in `src/sql_queries.sql`.

## Project Setup

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd "NHL Analytics Hub"
```

Replace the placeholder with the actual repository URL.

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the packages required by the project:

```bash
pip install pandas requests mysql-connector-python streamlit streamlit-option-menu jupyter
```

### 4. Configure Database Credentials

Create a local `.env` file or configure the environment variables used by the application. The database connection currently expects `NHL_DB_PASSWORD`.

For the current terminal session on macOS or Linux:

```bash
export NHL_DB_PASSWORD="your_mysql_password"
```

Do not commit `.env` files, passwords, or other credentials to GitHub.

### 5. Create and Populate the Database

Review the database setup and data-loading scripts before running them. Execute the appropriate setup and loading scripts in the required order so that tables and their dependencies exist before data is inserted.

Relevant scripts include:

- `database_setup.py`
- `create_tables.py`
- `load_teams.py`
- `src/load_standings.py`
- `src/load_players.py`
- `load_games.py`
- `load_game_stats.py`
- `load_skater_season_stats.py`
- `load_goalie_season_stats.py`

Run only the scripts required for your current database setup.

### 6. Run the Dashboard

```bash
streamlit run app.py
```

Streamlit will provide a local URL in the terminal to open the dashboard in your browser.

## Jupyter Notebook

The `notebooks/Day1_API_Exploration.ipynb` notebook documents the initial API exploration and data analysis workflow.

The notebook is used to explore API responses, inspect structured data, and validate the standings dataset.

## Current Project Progress

- NHL standings API exploration.
- Data cleaning and validation.
- Team performance analysis.
- MySQL database setup and data loading.
- Streamlit dashboard development.
- SQL-based data analysis.

## Future Improvements

- Add automated API data refresh.
- Improve data-loading automation and validation.
- Expand analytical queries and visualizations.
- Document the complete database schema and relationships.
- Add automated tests for data processing and database operations.

## Security Notes

- Keep credentials in environment variables or a local `.env` file.
- Never commit passwords, API secrets, or private credentials.
- Exclude virtual environments, cache files, and temporary files from version control.

## Author

NHL Analytics Hub — NHL data exploration, relational database analytics, and interactive visualization.
