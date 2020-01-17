import requests

source = requests.get("https://stats.nba.com/players/list/").json()

for team in source['data']:
    print("\n%s players\n" % team['home_route'].capitalize())
    for player in team['home_players']:
        print(player['name'])
    print("\n%s players\n" % team['away_route'].capitalize())
    for player in team['away_players']:
        print(player['name'])