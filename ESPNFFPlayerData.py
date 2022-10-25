import requests
import pandas as pd
import numpy as np


def load_league(league_id, year, week, swid, espn_s2):
    '''
    Load the matchup data for a given week, year with the
    proper cookie parameters 
    
    '''

    
    url = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/{year}/segments/0/leagues/{league_id}"

    # Make a request to the ESPN API
    league_response = requests.get(url + '?view=mMatchup&view=mMatchupScore',
                       params={'scoringPeriodId': week, 'matchupPeriodId': week},
                       cookies={"SWID": swid, "espn_s2": espn_s2})



    # Transform response into a JSON string
    league_json = league_response.json()
    
    return league_json

def load_player_data(league_json, week):
    

    # Initialize empty list for player scores, names, roster slot, fantasy team, week
    player_name = []
    player_score_act = []
    player_score_proj = []
    player_roster_slot = []
    player_fantasy_team = []
    weeks = []


    # Loop through each team
    for team in range(0, len(league_json['teams'])):
        
        # Loop through each roster slot in each team
        for slot in range(0, len(league_json['teams'][team]['roster']['entries'])):
            # Append the week number to a list for each entry for each team
            weeks.append(week)
            # Append player name, player fantasy team, and player ro
            player_name.append(league_json['teams'][team]['roster']['entries'][slot]['playerPoolEntry']['player']['fullName'])
            player_fantasy_team.append(league_json['teams'][team]['id'])
            player_roster_slot.append(league_json['teams'][team]['roster']['entries'][slot]['lineupSlotId'])
                

            # Loop through each statistic set for each roster slot for each team
            # to get projected and actual scores
            for stat in league_json['teams'][team]['roster']['entries'][slot]['playerPoolEntry']['player']['stats']:
                if stat['scoringPeriodId'] != week:
                    continue
                if stat['statSourceId'] == 0:
                    act = stat['appliedTotal']
                elif stat['statSourceId'] == 1:
                    proj = stat['appliedTotal']
                else:
                    print('Error')

            player_score_act.append(act)
            player_score_proj.append(proj)



    # Put the lists into a dictionary
    player_dict = {
        'Week' : weeks,
        'PlayerName' : player_name,
        'PlayerScoreActual' : player_score_act,
        'PlayerScoreProjected': player_score_proj,
        'PlayerRosterSlotId' : player_roster_slot,
        'PlayerFantasyTeam' : player_fantasy_team
    }
    
    # Transform the dictionary into a DataFrame
    df = pd.DataFrame.from_dict(player_dict)
    
    # Initialize empty column for PlayerRosterSlot
    df['PlayerRosterSlot'] = ""
    
    # Ignore chained assignment warnings
    pd.options.mode.chained_assignment = None
    
    # Replace the PlayerRosterSlot integers with position indicators
    for slot in df.index:
        
        if df['PlayerRosterSlotId'][slot] == 0:
            df['PlayerRosterSlot'][slot] = 'QB'
            
        if df['PlayerRosterSlotId'][slot] == 4:
            df['PlayerRosterSlot'][slot] = 'WR'
            
        if df['PlayerRosterSlotId'][slot] == 2:
            df['PlayerRosterSlot'][slot] = 'RB'
            
        if df['PlayerRosterSlotId'][slot] == 23:
            df['PlayerRosterSlot'][slot] = 'FLEX'
            
        if df['PlayerRosterSlotId'][slot] == 6:
            df['PlayerRosterSlot'][slot] = 'TE'
            
        if df['PlayerRosterSlotId'][slot] == 16:
            df['PlayerRosterSlot'][slot] = 'D/ST'
            
        if df['PlayerRosterSlotId'][slot] == 17:
            df['PlayerRosterSlot'][slot] = 'K'
            
        if df['PlayerRosterSlotId'][slot] == 20:
            df['PlayerRosterSlot'][slot] = 'Bench'
            
        if df['PlayerRosterSlotId'][slot] == 21:
            df['PlayerRosterSlot'][slot] = 'IR'
        
        if df['PlayerRosterSlotId'][slot] == '':
             df['PlayerRosterSlot'][slot] = 'NA'
    
    df = df.drop(columns=['PlayerRosterSlotId'])
    
    
    return df

def load_team_names(df, league_id, year, week, swid, espn_s2):
    '''
    Load the fantasy owner team names and join them to our player DataFrame
    
    '''
    
    
    # Define the URL with our parameters
    url = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/{year}/segments/0/leagues/{league_id}"
    
    # Get a response from the ESPN API using the Team view
    team_response = requests.get(url, 
                                params={"leagueId" : league_id,
                                       "seasonId" : year,
                                       "matchupPeriodId" : week,
                                       "view": "mTeam"},
                               cookies={"swid" : swid,
                                       "espn_s2" : espn_s2})
    
    # Transform the response into a JSON
    team_json = team_response.json()

    # Initialize empty list for team names and team ids
    team_id = []
    team_primary_owner = []
    team_location = []
    team_nickname = []
    owner_first_name = []
    owner_last_name = []
    team_cookie = []

    # Loop through each team in the JSON
    for team in range(0, len(team_json['teams'])):
        # Append the team id and team name to the list
        team_id.append(team_json['teams'][team]['id'])
        team_primary_owner.append(team_json['teams'][team]['primaryOwner'])
        team_location.append(team_json['teams'][team]['location'])
        team_nickname.append(team_json['teams'][team]['nickname'])
        owner_first_name.append(team_json['members'][team]['firstName'])
        owner_last_name.append(team_json['members'][team]['lastName'])
        team_cookie.append(team_json['members'][team]['id'])
    
    
    # Create team DataFrame
    team_df = pd.DataFrame({
    'PlayerFantasyTeam': team_id,
    'TeamPrimaryOwner': team_primary_owner,
    'Location': team_location,
    'Nickname': team_nickname,
    })

    # Create owner DataFrame
    owner_df = pd.DataFrame({
    'OwnerFirstName': owner_first_name,
    'OwnerLastName': owner_last_name,
    'TeamPrimaryOwner': team_cookie
    })

    # Merge the team and owner DataFrames on the TeamPrimaryOwner column
    team_df = pd.merge(team_df, owner_df, on='TeamPrimaryOwner', how='left')

    # Filter team_df to only include PlayerFantasyTeam, Location, Nickname, OwnerFirstName, and OwnerLastName
    team_df = team_df[['PlayerFantasyTeam', 'Location', 'Nickname', 'OwnerFirstName', 'OwnerLastName']]
    
    # Concatenate the two name columns
    team_df['TeamName'] = team_df['Location'] + ' ' + team_df['Nickname']

    # Create a column for full name
    team_df['FullName'] = team_df['OwnerFirstName'] + ' ' + team_df['OwnerLastName']

    # Drop all columns except id and Name
    team_df = team_df.filter(['PlayerFantasyTeam', 'TeamName', 'FullName'])
    
    # Merge DataFrames to get team names instead of ids and rename Name column to Name1
    df = df.merge(team_df, on=['PlayerFantasyTeam'], how='left')
    df = df.rename(columns={'Name':'PlayerFantasyTeamName'})
    
    return df
    

