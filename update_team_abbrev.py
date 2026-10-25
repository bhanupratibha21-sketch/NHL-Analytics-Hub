import mysql.connector

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",

    database="nhl_analytics"
)

cursor = connection.cursor()

# Team name to abbreviation mapping
team_mapping = {
    "Anaheim Ducks": "ANA",
    "Boston Bruins": "BOS",
    "Buffalo Sabres": "BUF",
    "Carolina Hurricanes": "CAR",
    "Columbus Blue Jackets": "CBJ",
    "Calgary Flames": "CGY",
    "Chicago Blackhawks": "CHI",
    "Colorado Avalanche": "COL",
    "Dallas Stars": "DAL",
    "Detroit Red Wings": "DET",
    "Edmonton Oilers": "EDM",
    "Florida Panthers": "FLA",
    "Los Angeles Kings": "LAK",
    "Minnesota Wild": "MIN",
    "Montreal Canadiens": "MTL",
    "New Jersey Devils": "NJD",
    "Nashville Predators": "NSH",
    "New York Islanders": "NYI",
    "New York Rangers": "NYR",
    "Ottawa Senators": "OTT",
    "Philadelphia Flyers": "PHI",
    "Pittsburgh Penguins": "PIT",
    "Seattle Kraken": "SEA",
    "San Jose Sharks": "SJS",
    "St. Louis Blues": "STL",
    "Tampa Bay Lightning": "TBL",
    "Toronto Maple Leafs": "TOR",
    "Utah Mammoth": "UTA",
    "Vancouver Canucks": "VAN",
    "Vegas Golden Knights": "VGK",
    "Winnipeg Jets": "WPG",
    "Washington Capitals": "WSH"
}

# Update team abbreviations
update_query = """
UPDATE teams
SET team_abbrev = %s
WHERE team_name = %s
"""

for team_name, abbreviation in team_mapping.items():
    cursor.execute(update_query, (abbreviation, team_name))

# Save changes
connection.commit()

print(f"{cursor.rowcount} teams updated successfully!")

# Close connection
cursor.close()
connection.close()
