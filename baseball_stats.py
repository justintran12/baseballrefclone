import statsapi

# helper functions that contain api calls to MLB stats api to get data

# returns map of player's career stats: {'gamesPlayed': '206', 'groundOuts': '162', etc.}
# return None if input incorrect type for player (when input pitcher for a hitter or vice versa)
# errors out if not given an active player name
def getPlayerCareerStats(player_name, player_type):
	curr_season = statsapi.latest_season()['seasonId']
	id = next(x['id'] for x in statsapi.get('sports_players',{'season':curr_season,'gameType':'W'})['people'] if x['fullName']== player_name)
	player_stats_str = statsapi.player_stats(id, player_type, 'career')
	split_str = "Career Hitting" if player_type == "hitting" else "Career Pitching"
	player_stats_split = player_stats_str.split(split_str)
	# handles incorrect type for player case
	if len(player_stats_split) < 2:
		return None

	player_stats_arr = player_stats_str.split(split_str)[1].strip().split("\n")

	player_stats_map = {}
	for stat in player_stats_arr:
		stat_arr = stat.split(":")
		stat_name = stat_arr[0].strip()
		stat_val = stat_arr[1].strip()
		player_stats_map[stat_name] = stat_val
		
	return player_stats_map

# return map of player's stats by season: {'2023': {'gamesPlayed' : '206, 'groundOuts' : '162, etc.}, '2022' : {...}, etc.}
# returns empty map if input incorrect player type for the player (ex: input pitcher type for a hitter)
# errors out if not given an active player name
def getPlayerSeasonStats(player_name, player_type):
	curr_season = statsapi.latest_season()['seasonId']
	id = next(x['id'] for x in statsapi.get('sports_players',{'season':curr_season,'gameType':'W'})['people'] if x['fullName']== player_name)

	#lookup_player function might be buggy, so not using it for now
	#id = statsapi.lookup_player(player_name)[0]['id']

	stats_seasons_map = {}
	for season_data in statsapi.player_stat_data(id, group=player_type, type="yearByYear", sportId=1)['stats']:
		year = season_data['season']
		stats_seasons_map[year] = season_data['stats']
	
	return stats_seasons_map
	
# return map of current season league leaders, ex: {'ERA' : [[1, 'Shane McClanahan', 'Tampa Bay Rays', '2.02'], [2, 'Eduardo Rodriguez', 'Detroit Tigers', '2.13'], ...], 'WHIP' : ..., etc.}
def getLeagueLeaders():
	curr_season = statsapi.latest_season()['seasonId']

	era_leaders = statsapi.league_leader_data('earnedRunAverage',statGroup='pitching',limit=100,season=curr_season) 
	whip_leaders = statsapi.league_leader_data('walksAndHitsPerInningPitched',statGroup='pitching',limit=100,season=curr_season) 
	so_leaders = statsapi.league_leader_data('strikeouts',statGroup='pitching',limit=100,season=curr_season) 
	ip_leaders = statsapi.league_leader_data('inningsPitched',statGroup='pitching',limit=100,season=curr_season) 
	ba_leaders = statsapi.league_leader_data('battingAverage',statGroup='hitting',limit=100,season=curr_season) 
	obp_leaders = statsapi.league_leader_data('onBasePercentage',statGroup='hitting',limit=100,season=curr_season) 
	slg_leaders = statsapi.league_leader_data('sluggingPercentage',statGroup='hitting',limit=100,season=curr_season) 
	ops_leaders = statsapi.league_leader_data('onBasePlusSlugging',statGroup='hitting',limit=100,season=curr_season) 
	hit_leaders = statsapi.league_leader_data('hits',statGroup='hitting',limit=100,season=curr_season) 
	hr_leaders = statsapi.league_leader_data('homeRuns',statGroup='hitting',limit=100,season=curr_season) 
	sb_leaders = statsapi.league_leader_data('stolenBases',statGroup='hitting',limit=100,season=curr_season) 
	rbi_leaders = statsapi.league_leader_data('runsBattedIn',statGroup='hitting',limit=100,season=curr_season) 

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

# return map of team leader's data, ex: {'ERA': [[1, 'Luis Castillo', '2.70'], [2, 'George Kirby', '3.50'], [3, 'Logan Gilbert', '3.80']], 'SO9': [[1, 'Luis Castillo', '10.80'], ... ], etc. }
# throws 404 client error if given invalid team id
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
	
# helper function for getRosterData(team_id)
# input format: ['#8', 'DH', 'AJ', 'Pollock']
# can sometimes have cases like: ['#23', 'CF', 'Michael', 'Harris', 'II'] or ['#13', 'RF', 'Ronald', 'Acuna', 'Jr.']
# so can't just take the last 2 elements in array all the time
# ex output: "AJ Pollock"
def getRosterPlayerName(player_data):
	player_name = "" 
	for i in range(2,len(player_data) - 1):
		player_name += player_data[i] + " "
	player_name += player_data[len(player_data) - 1]

	return player_name

# returns player stats for current season for active players on 40-man roster of the input team
# ex output: {'#33  P   A.J. Minter': {'gamesPlayed': 31, 'gamesStarted': 0, ... , 'year': '2023'}, '#62  P   AJ Smith-Shawver': {'gamesPlayed': 2, ... } }
def getRosterData(team_id):
	roster = statsapi.roster(team_id).split("\n") 
	roster_map = {}
	curr_season = statsapi.latest_season()['seasonId']
	for player in roster:
		# empty arrays result from splitting roster on "\n", this if case handles that
		if len(player) > 0:
			player_data = player.split()
			player_name = getRosterPlayerName(player_data)
			position =  player_data[1]
			player_id = next(x['id'] for x in statsapi.get('sports_players',{'season':curr_season,'gameType':'W'})['people'] if x['fullName']== player_name)
			player_type = "pitching" if position == 'P' else "hitting"
			player_stats_data = statsapi.player_stat_data(player_id, group=player_type, type="season", sportId=1)['stats']
			# can sometimes have empty player_stats_data returned, in that case do not add that player to roster
			if len(player_stats_data) > 0:
				player_stats = player_stats_data[0]['stats']
				player_stats['year'] = curr_season
				roster_map[player] = player_stats

	return roster_map

# helper function to convert team name from string input from user to its corresponding id
def teamNameToId(team_name):
	team = statsapi.lookup_team(team_name)
	team_id = team[0]['id']
	return team_id

# ex out: {'div_name': 'American League West', 'teams': [{'name': 'Texas Rangers', 'div_rank': '1', ... }, {'name': 'Houston Astros', 'div_rank': '2', ... } ] }
def getTeamStandingsData(team_id):
	league = statsapi.get('team', {'teamId':team_id})['teams'][0]['league']['id']
	division = statsapi.get('team', {'teamId':team_id})['teams'][0]['division']['id']
	div_standings_map = statsapi.standings_data(leagueId = league)[division]
	return div_standings_map

# helper to get player type (hitter or pitcher) of input player
# errors out if not given active player 
def getPlayerType(player_name):
	curr_season = statsapi.latest_season()['seasonId']
	player_info = next(x for x in statsapi.get('sports_players',{'season':curr_season,'gameType':'W'})['people'] if x['fullName']== player_name)
	player_type = player_info['primaryPosition']['type']

	return "pitching" if player_type == "Pitcher" else "hitting"

def playerOrTeam(input_name):
	if len(statsapi.lookup_player(input_name)) == 1:
		return "player"
	elif len(statsapi.lookup_team(input_name)) == 1:
		return "team"
	else:
		return None
