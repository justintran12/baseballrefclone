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

team = statsapi.lookup_team('Atlanta Braves')
team_id = team[0]['id']
#league = statsapi.get('team', {'teamId':team_id})['teams'][0]['league']['id']
#division = statsapi.get('team', {'teamId':team_id})['teams'][0]['division']['id']
#print( statsapi.roster(id).split("\n") )
#print(statsapi.standings_data(leagueId = league)[division])
print(statsapi.team_leader_data(team_id, "strikeoutsPer9Inn"))

def getRosterData(team_id):
    roster = statsapi.roster(team_id).split("\n") 
    roster_map = {}
    curr_season = statsapi.latest_season()['seasonId']
    for player in roster:
        if len(player) > 0:
            player_data = player.split()
            player_name = "" 
            for i in range(2,len(player_data) - 1):
                player_name += player_data[i] + " "
            player_name += player_data[len(player_data) - 1]
            position =  player_data[1]
            id = next(x['id'] for x in statsapi.get('sports_players',{'season':curr_season,'gameType':'W'})['people'] if x['fullName']== player_name)
            player_type = "pitching" if position == 'P' else "hitting"
            player_stats_data = statsapi.player_stat_data(id, group=player_type, type="season", sportId=1)['stats']
            if len(player_stats_data) > 0:
                player_stats = player_stats_data[0]['stats']
                player_stats['year'] = curr_season
                roster_map[player] = player_stats

    return roster_map

#print(getRosterData(team_id))