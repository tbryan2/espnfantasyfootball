# ESPN-API
[Video Tutorial](https://youtu.be/m9Qs1kk4lOo)

## Parameters

### league_id
Log into your ESPN Fantasy Football league and locate the URL parameter that says &leagueId=123456. This 6 digit number is your ESPN league id. Paste this into your config.py file.

### swid & espn_s2
These are both cookie parameters, which you can find by first logging into your ESPN Fantasy Football league. Then, right click anywhere on the webpage in your browser and click Inspect Element. Navigate to the Storage tab in your browser's dev tools. Locate the cookies stored by ESPN.com and copy the swid and espn_s2 cookies. Hint: keep the swid cookie within the curly brackets {}. Paste them both in the config.py file.

## Functions

1. Load the parameters from your config.py file and feed them through the load_league function (this returns a JSON string):
```
# Import config file elements
from config import league_id, swid, espn_s2

league_id = league_id
swid = swid
espn_s2 = espn_s2

# Define year and week
year = 2022
week = 1

# Feed parameters into load_league function
league = load_league(league_id, year, week, swid, espn_s2)
```

2. Feed the league JSON variable into the load_player_data function (this returns a pandas DataFrame):

```

# Feed parameters into load_player_data function
df = load_player_data(league, week)
```
3. Before manipulating the DataFrame returned from the last function, run load_team_names to replace generic team ids with actual team names:
```
# Feed parameeters into load_team_names function
df = load_team_names(df, league_id, year, week, swid, espn_s2)
```
