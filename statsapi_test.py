# file for testing statsapi functions
import statsapi

player_name = 'Aaron Judge'
id = next(x['id'] for x in statsapi.get('sports_players',{'season':2023,'gameType':'W'})['people'] if x['fullName']== player_name)

stats_seasons_map = {}
for season_data in statsapi.player_stat_data(id, group="hitting", type="yearByYear", sportId=1)['stats']:
    year = season_data['season']
    stats_seasons_map[year] = season_data['stats']

print(statsapi.player_stat_data(id, group="hitting", type="yearByYear", sportId=1))