-- Query 1: Total number of games
SELECT
    COUNT(*) AS total_games
FROM games;


-- Query 2: Home vs Away goals
SELECT
    SUM(home_score) AS total_home_goals,
    SUM(away_score) AS total_away_goals,
    ROUND(AVG(home_score), 2) AS avg_home_goals,
    ROUND(AVG(away_score), 2) AS avg_away_goals
FROM games;


-- Query 3: Highest-scoring games
SELECT
    game_id,
    game_date,
    home_team_abbrev,
    away_team_abbrev,
    home_score,
    away_score,
    (home_score + away_score) AS total_goals
FROM games
ORDER BY total_goals DESC
LIMIT 10;


-- Query 4: Biggest winning margins
SELECT
    game_id,
    game_date,
    home_team_abbrev,
    away_team_abbrev,
    home_score,
    away_score,
    ABS(home_score - away_score) AS winning_margin
FROM games
ORDER BY winning_margin DESC
LIMIT 10;


-- Query 5: Games by venue
SELECT
    venue_name,
    COUNT(*) AS total_games
FROM games
GROUP BY venue_name
ORDER BY total_games DESC
LIMIT 10;


-- Query 6: Home team wins
SELECT
    home_team_abbrev AS team,
    COUNT(*) AS home_wins
FROM games
WHERE home_score > away_score
GROUP BY home_team_abbrev
ORDER BY home_wins DESC;


-- Query 7: Away team wins
SELECT
    away_team_abbrev AS team,
    COUNT(*) AS away_wins
FROM games
WHERE away_score > home_score
GROUP BY away_team_abbrev
ORDER BY away_wins DESC;


-- Query 8: Total wins by team
SELECT
    team,
    SUM(wins) AS total_wins
FROM (
    SELECT
        home_team_abbrev AS team,
        COUNT(*) AS wins
    FROM games
    WHERE home_score > away_score
    GROUP BY home_team_abbrev

    UNION ALL

    SELECT
        away_team_abbrev AS team,
        COUNT(*) AS wins
    FROM games
    WHERE away_score > home_score
    GROUP BY away_team_abbrev
) AS team_wins
GROUP BY team
ORDER BY total_wins DESC;


-- Query 9: Total goals scored by each team
SELECT
    team,
    SUM(goals_for) AS total_goals
FROM (
    SELECT
        home_team_abbrev AS team,
        SUM(home_score) AS goals_for
    FROM games
    GROUP BY home_team_abbrev

    UNION ALL

    SELECT
        away_team_abbrev AS team,
        SUM(away_score) AS goals_for
    FROM games
    GROUP BY away_team_abbrev
) AS team_goals
GROUP BY team
ORDER BY total_goals DESC;


-- Query 10: Average goals per game
SELECT
    ROUND(AVG(home_score + away_score), 2) AS avg_total_goals
FROM games;



-- Query 11: Top teams by goals scored
SELECT
    team_name,
    team_abbrev,
    goals_for,
    goals_against,
    (goals_for - goals_against) AS goal_difference
FROM teams
ORDER BY goals_for DESC
LIMIT 10;



-- Query 12: Teams above league average points
SELECT
    team_name,
    team_abbrev,
    points
FROM teams
WHERE points > (
    SELECT AVG(points)
    FROM teams
)
ORDER BY points DESC;



-- Query 13: Venues with more than 40 games
SELECT
    venue_name,
    COUNT(*) AS total_games
FROM games
GROUP BY venue_name
HAVING COUNT(*) > 40
ORDER BY total_games DESC;


-- Query 14: Total number of players
SELECT
    COUNT(*) AS total_players
FROM players;


-- Query 15: Players by position
SELECT
    position,
    COUNT(*) AS player_count
FROM players
GROUP BY position
ORDER BY player_count DESC;


-- Query 16: Player count by team
SELECT
    t.team_name,
    t.team_abbrev,
    COUNT(p.player_id) AS player_count
FROM teams t
LEFT JOIN players p
    ON t.team_id = p.team_id
GROUP BY t.team_id, t.team_name, t.team_abbrev
ORDER BY player_count DESC;


-- Query 17: Player details with team
SELECT
    p.player_name,
    p.position,
    p.jersey_number,
    t.team_name,
    t.team_abbrev
FROM players p
JOIN teams t
    ON p.team_id = t.team_id
ORDER BY t.team_name, p.player_name
LIMIT 50;


-- Query 18: Team home and away wins
SELECT
    t.team_name,
    s.home_wins,
    s.away_wins,
    (s.home_wins + s.away_wins) AS total_wins
FROM standings s
JOIN teams t
    ON s.team_id = t.team_id
ORDER BY total_wins DESC;