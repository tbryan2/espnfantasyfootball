import os
import espnfantasyfootball as espn
import pandas as pd

# Read the league ID, swid, and espn_s2 from the environment
LEAGUE_ID = os.environ.get('LEAGUE_ID')
SWID = os.environ.get('SWID')
ESPN_S2 = os.environ.get('ESPN_S2')

league = espn.FantasyLeague(league_id=LEAGUE_ID, year=2023,
                            swid=SWID, espn_s2=ESPN_S2)

player_data = league.get_league_data()
player_data.to_csv('output/player_data.csv', index=False)

matchup_data = league.get_matchup_data()
matchup_data.to_csv('output/matchup_data.csv', index=False)
