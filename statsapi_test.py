# file for testing statsapi functions
import statsapi

player_name = 'George Kirby'
id = next(x['id'] for x in statsapi.get('sports_players',{'season':2023,'gameType':'W'})['people'] if x['fullName']== player_name)

'''
stats_seasons_map = {}
for season_data in statsapi.player_stat_data(id, group="pitching", type="yearByYear", sportId=1)['stats']:
    year = season_data['season']
    stats_seasons_map[year] = season_data['stats']

print(statsapi.player_stats(id, 'pitching', 'career').split("Career Pitching")[1].strip().split("\n"))
'''

team = statsapi.lookup_team('Seattle Mariners')
team_id = team[0]['id']
#print( statsapi.roster(id).split("\n") )
#print(statsapi.get('team', {'teamId':id}))

def getRosterData(team_id):
    roster = statsapi.roster(team_id).split("\n") 
    roster_map = {}
    curr_season = statsapi.latest_season()['seasonId']
    for player in roster:
        if len(player) > 0:
            player_data = player.split()
            player_name = player_data[2] + " " + player_data[3]
            position =  player_data[1]
            id = next(x['id'] for x in statsapi.get('sports_players',{'season':curr_season,'gameType':'W'})['people'] if x['fullName']== player_name)
            player_type = "pitching" if position == 'P' else "hitting"
            player_stats = statsapi.player_stat_data(id, group=player_type, type="season", sportId=1)['stats'][0]['stats']
            player_stats['year'] = curr_season
            roster_map[player] = player_stats

    return roster_map

print(getRosterData(team_id))