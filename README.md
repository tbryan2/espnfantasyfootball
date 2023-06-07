# espnfantasyfootball
`pip install espnfantasyfootball`

### Security Requirements
You will need to find your _league_id_ as well as the _swid_ and _espn_s2_ cookie parameters for your league. The league_id is found in the URL of your fantasy league:

<p align="center">
  <img width="832" alt="Screenshot 2023-06-07 at 11 52 16 AM" src="https://github.com/tbryan2/espnfantasyfootball/assets/29851231/2d40e807-644c-4423-bb70-5862c3fdd295">
</p>

To find the swid and espn_s2 cookie parameters, go to you any page on your fantasy league's website. Right click on the page and hit __Inspect Element__. Locate the _Storage_ tab in your browser's developer tools and find _Cookies_. Locate these two cookie parameters and copy them into a secrets.py file to be imported later.

## FantasyLeague
Create a FantasyLeague object by importing the package and instantiating the class:
```
import espnfantasyfootball as espn
import pandas as pd
import secrets

league = espn.FantasyLeague(league_id=730129, year=2022,
                            swid=secrets.swid, espn_s2=secrets.espn_s2)
```

## Pulling Data
Now that we have the league object created, we can pull data. You can pull player data as well as league matchup data: 
 
 
`player_data = league.get_league_data()` 

`print(player_data)`
```python
| Week | PlayerName           | PlayerScoreActual | PlayerScoreProjected | PlayerFantasyTeam   | PlayerRosterSlot | TeamName                 | FullName    |
|------|----------------------|------------------|---------------------|---------------------|------------------|--------------------------|-------------|
| 0    | Derrick Henry        | 16.1             | 17.382072           | 1                   | RB               | Pfizer Save us           | Toker Blaze |
| 1    | Aaron Jones          | 17.6             | 15.289672           | 1                   | RB               | Pfizer Save us           | Toker Blaze |
| 2    | George Kittle        | 9.3              | 15.967135           | 1                   | TE               | Pfizer Save us           | Toker Blaze |
| 3    | Robert Woods         | 17.9             | 14.470935           | 1                   | WR               | Pfizer Save us           | Toker Blaze |
| 4    | JuJu Smith-Schuster  | 24.9             | 14.596111           | 1                   | WR               | Pfizer Save us           | Toker Blaze |
| ...  | ...                  | ...              | ...                 | ...                 | ...              | ...                      | ...         |
| 157  | Preston Williams     | 0.0              | 0.000000            | 14                  | Bench            | Edinburgh Chubby chasers | John Meier  |
| 158  | Zane Gonzalez        | 0.0              | 0.000000            | 14                  | K                | Edinburgh Chubby chasers | John Meier  |
| 159  | Cowboys D/ST         | 12.1             | 12.143736           | 14                  | Bench            | Edinburgh Chubby chasers | John Meier  |
| 160  | Myles Gaskin         | 17.7             | 16.453915           | 14                  | Bench            | Edinburgh Chubby chasers | John Meier  |
| 161  | J.D. McKissic        | 8.0              | 13.152776           | 14                  | RB               | Edinburgh Chubby chasers | John Meier  |
```
`matchup_data = league.get_matchup_data()` 

`print(matchup_data)`
```python
| Week | Name1                    | Score1 | Name2                 | Score2 | Type    |
|------|--------------------------|--------|-----------------------|--------|---------|
| 0    | Edinburgh Chubby chasers | 93.49  | The Masked Singers    | 135.95 | Regular |
| 1    | Happy Hanukkah           | 146.31 | The Cumbacks          | 130.68 | Regular |
| 2    | Titsburgh Feelers        | 145.97 | Hooked on a Thielen   | 181.15 | Regular |
| 3    | Gonq Unicorns            | 153.85 | 3rd Place Pays Out    | 89.58  | Regular |
| 4    | Tame Klonger             | 111.03 | Pfizer Save us        | 149.84 | Regular |
| ...  | ...                      | ...    | ...                   | ...    | ...     |
| 1287 | Gonq Unicorns            | 128.72 | The Masked Singers    | 119.15 | Playoff |
| 1288 | Hooked on a Thielen      | 114.22 | Pfizer Save us        | 168.56 | Playoff |
| 1289 | Titsburgh Feelers        | 160.07 | Tame Klonger          | 143.83 | Playoff |
| 1290 | 3rd Place Pays Out       | 70.81  | Edinburgh Chubby chasers | 123.26 | Playoff |
| 1291 | The Cumbacks             | 84.00  | Happy Hanukkah        | 155.73 | Playoff |
```

By default, the functions will pull the full year of data but an optional `week=` parameter can be supplied to pull specific weeks.
