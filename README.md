# ESPN-API
[Video Tutorial](https://youtu.be/8W-NuLjbzGI)

## Objective
Use these pre-built functions that call the ESPN API and package your fantasy league's data nicely:

- load_league(league_id, year, week, swid, espn_s2): outputs a JSON string of data for the given week and year

- load_player_data(matchup_json, week, league_size, roster_size): outputs a clean DataFrame of every team's roster, player projections, player performance, etc.

- load_team_names(df, league_id, year, week, swid, espn_s2): replaces the team id with actual ESPN fantasy team names
