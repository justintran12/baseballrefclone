import statsapi

# helper functions that contain api calls to MLB stats api to get data
def getPlayerCareerStats(player_name, player_type):
	curr_season = statsapi.latest_season()['seasonId']
	id = next(x['id'] for x in statsapi.get('sports_players',{'season':curr_season,'gameType':'W'})['people'] if x['fullName']== player_name)
	player_stats_str = statsapi.player_stats(id, player_type, 'career')
	split_str = "Career Hitting" if player_type == "hitting" else "Career Pitching"
	player_stats_arr = player_stats_str.split(split_str)[1].strip().split("\n")

	player_stats_map = {}
	for stat in player_stats_arr:
		stat_arr = stat.split(":")
		stat_name = stat_arr[0].strip()
		stat_val = stat_arr[1].strip()
		player_stats_map[stat_name] = stat_val
		
	return player_stats_map

def getPlayerSeasonStats(player_name, player_type):
	curr_season = statsapi.latest_season()['seasonId']
	id = next(x['id'] for x in statsapi.get('sports_players',{'season':curr_season,'gameType':'W'})['people'] if x['fullName']== player_name)

	stats_seasons_map = {}
	for season_data in statsapi.player_stat_data(id, group=player_type, type="yearByYear", sportId=1)['stats']:
		year = season_data['season']
		stats_seasons_map[year] = season_data['stats']
	
	return stats_seasons_map
	
def getLeagueLeaders():
	era_leaders = statsapi.league_leader_data('earnedRunAverage',statGroup='pitching',limit=100,season=2023) 
	whip_leaders = statsapi.league_leader_data('walksAndHitsPerInningPitched',statGroup='pitching',limit=100,season=2023) 
	so_leaders = statsapi.league_leader_data('strikeouts',statGroup='pitching',limit=100,season=2023) 
	ip_leaders = statsapi.league_leader_data('inningsPitched',statGroup='pitching',limit=100,season=2023) 
	ba_leaders = statsapi.league_leader_data('battingAverage',statGroup='hitting',limit=100,season=2023) 
	obp_leaders = statsapi.league_leader_data('onBasePercentage',statGroup='hitting',limit=100,season=2023) 
	slg_leaders = statsapi.league_leader_data('sluggingPercentage',statGroup='hitting',limit=100,season=2023) 
	ops_leaders = statsapi.league_leader_data('onBasePlusSlugging',statGroup='hitting',limit=100,season=2023) 
	hit_leaders = statsapi.league_leader_data('hits',statGroup='hitting',limit=100,season=2023) 
	hr_leaders = statsapi.league_leader_data('homeRuns',statGroup='hitting',limit=100,season=2023) 
	sb_leaders = statsapi.league_leader_data('stolenBases',statGroup='hitting',limit=100,season=2023) 
	rbi_leaders = statsapi.league_leader_data('runsBattedIn',statGroup='hitting',limit=100,season=2023) 

	leader_stats = {}
	leader_stats['ERA'] = era_leaders
	leader_stats['WHIP'] = whip_leaders
	leader_stats['SO'] = so_leaders
	leader_stats['IP'] = ip_leaders
	leader_stats['BA'] = ba_leaders
	leader_stats['OBP'] = obp_leaders
	leader_stats['SLG'] = slg_leaders
	leader_stats['OPS'] = ops_leaders
	leader_stats['Hits'] = hit_leaders
	leader_stats['HR'] = hr_leaders
	leader_stats['SB'] = sb_leaders
	leader_stats['RBI'] = rbi_leaders

	return leader_stats

def getTeamLeadersData(team_id):
	leader_stats = {}
	leader_stats['ERA'] = statsapi.team_leader_data(team_id, "earnedRunAverage")
	leader_stats['SO9'] = statsapi.team_leader_data(team_id, "strikeoutsPer9Inn")
	leader_stats['WHIP'] = statsapi.team_leader_data(team_id, "walksAndHitsPerInningPitched")
	leader_stats['IP'] = statsapi.team_leader_data(team_id, "inningsPitched")
	leader_stats['BA'] = statsapi.team_leader_data(team_id, "battingAverage")
	leader_stats['OBP'] = statsapi.team_leader_data(team_id, "onBasePercentage")
	leader_stats['SLG'] = statsapi.team_leader_data(team_id, "sluggingPercentage")
	leader_stats['OPS'] = statsapi.team_leader_data(team_id, "onBasePlusSlugging")
	leader_stats['Hits'] = statsapi.team_leader_data(team_id, "hits")
	leader_stats['HR'] = statsapi.team_leader_data(team_id, "homeRuns")
	leader_stats['SB'] = statsapi.team_leader_data(team_id, "stolenBases")
	leader_stats['RBI'] = statsapi.team_leader_data(team_id, "runsBattedIn")
	leader_stats['Saves'] = statsapi.team_leader_data(team_id, "saves")
	
	return leader_stats
	
def getRosterPlayerName(player_data):
	player_name = "" 
	for i in range(2,len(player_data) - 1):
		player_name += player_data[i] + " "
	player_name += player_data[len(player_data) - 1]

	return player_name

def getRosterData(team_id):
	roster = statsapi.roster(team_id).split("\n") 
	roster_map = {}
	curr_season = statsapi.latest_season()['seasonId']
	for player in roster:
		if len(player) > 0:
			player_data = player.split()
			player_name = getRosterPlayerName(player_data)
			position =  player_data[1]
			player_id = next(x['id'] for x in statsapi.get('sports_players',{'season':curr_season,'gameType':'W'})['people'] if x['fullName']== player_name)
			player_type = "pitching" if position == 'P' else "hitting"
			player_stats_data = statsapi.player_stat_data(player_id, group=player_type, type="season", sportId=1)['stats']
			if len(player_stats_data) > 0:
				player_stats = player_stats_data[0]['stats']
				player_stats['year'] = curr_season
				roster_map[player] = player_stats

	return roster_map

def teamNameToId(team_name):
	team = statsapi.lookup_team(team_name)
	team_id = team[0]['id']
	return team_id

def getTeamStandingsData(team_id):
	league = statsapi.get('team', {'teamId':team_id})['teams'][0]['league']['id']
	division = statsapi.get('team', {'teamId':team_id})['teams'][0]['division']['id']
	div_standings_map = statsapi.standings_data(leagueId = league)[division]
	return div_standings_map