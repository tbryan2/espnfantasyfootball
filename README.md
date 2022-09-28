# ESPN-API
[Video Tutorial](https://youtu.be/8W-NuLjbzGI)

## Parameters

**league_id** - log into your ESPN Fantasy Football league and locate the URL parameter that says &leagueId=123456. This 6 digit number is your ESPN league id.

**swid & espn_s2** - these are both cookie parameters, which you can find by first logging into your ESPN Fantasy Football league. Then, right click anywhere on the webpage in your browser and click Inspect Element. Navigate to the Storage tab in your browser's dev tools. Locate the cookies stored by ESPN.com and copy the swid and espn_s2 cookies. Hint: keep the swid cookie within the curly brackets {}. Paste them both in the config.py file.

## Functions
Use these pre-built functions that call the ESPN API and package your fantasy league's data nicely:

`load_league(league_id, year, week, swid, espn_s2)`

- load_player_data(matchup_json, week, league_size, roster_size): outputs a clean DataFrame of every team's roster, player projections, player performance, etc.

- load_team_names(df, league_id, year, week, swid, espn_s2): replaces the team id with actual ESPN fantasy team names
