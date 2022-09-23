def load_league(league_id, year, week, swid, espn_s2):
    '''
    Load the matchup data for a given week, year with the
    proper cookie parameters 
    
    '''
    import requests
    import pandas as pd
    import numpy as np
    
    url = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/{year}/segments/0/leagues/{league_id}"

    # Make a request to the ESPN API
    matchup_response = requests.get(url + '?view=mMatchup&view=mMatchupScore',
                       params={'scoringPeriodId': week, 'matchupPeriodId': week},
                       cookies={"SWID": swid, "espn_s2": espn_s2})



    # Transform response into a JSON string
    matchup_json = matchup_response.json()
    
    return matchup_json

def load_player_data(matchup_json, week, league_size, roster_size):
    
    import requests
    import pandas as pd
    import numpy as np
    

    # Initialize empty list for player scores, names, roster slot, fantasy team, week
    player_name = []
    player_score_act = []
    player_score_proj = []
    player_roster_slot = []
    player_fantasy_team = []
    weeks = []


    # Loop through each team
    for team in range(0, league_size):
        # Loop through each roster slot in each team
        for slot in range(0, 16):
            
            # Append the week number to a list for each entry for each team
            weeks.append(week)

            # Append player name, player fantasy team, and player ro
            player_name.append(matchup_json['teams'][team]['roster']['entries'][slot]['playerPoolEntry']['player']['fullName'])
            player_fantasy_team.append(matchup_json['teams'][team]['id'])
            player_roster_slot.append(matchup_json['teams'][team]['roster']['entries'][slot]['lineupSlotId'])

            # Loop through each statistic set for each roster slot for each team
            # to get projected and actual scores
            for stat in matchup_json['teams'][team]['roster']['entries'][slot]['playerPoolEntry']['player']['stats']:
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
    df = pd.DataFrame(player_dict)
    
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
    
    df.drop(df['PlayerRosterSlotId'])
    
    
    
    return df

def load_team_names(df, league_id, year, week, swid, espn_s2):
    '''
    Load the fantasy owner team names and join them to our player DataFrame
    
    '''
    
    import requests
    import pandas as pd
    import numpy as np
    
    
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
    
    # Normalize JSON into DataFrame
    team_df = pd.json_normalize(team_json['teams'])
    
    # Choose column names
    team_column_names = {
    'id':'PlayerFantasyTeam',
    'location':'Name1',
    'nickname':'Name2'
    }

    # Reindex based on column names
    team_df = team_df.reindex(columns=team_column_names).rename(columns=team_column_names)
    
    # Concatenate the two name columns
    team_df['Name'] = team_df['Name1'] + ' ' + team_df['Name2']

    # Drop all columns except id and Name
    team_df = team_df.filter(['PlayerFantasyTeam', 'Name'])
    

    # Merge DataFrames to get team names instead of ids and rename Name column to Name1
    df = df.merge(team_df, on=['PlayerFantasyTeam'], how='left')
    df.drop(df['PlayerFantasyTeam'])
    df = df.rename(columns={'Name':'PlayerFantasyTeamName'})
    
    
    
    return df
    