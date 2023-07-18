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
	'''
	elif len(statsapi.lookup_player(input_name)) > 1:
		return "multi-players"
	elif len(statsapi.lookup_team(input_name))  > 1:
		return "multi-teams"
	'''

# lookup_player and lookup_team will return empty list if player/team does not exist. Both methods can also return multiple players/teams that match the input (ie: new york has 2 teams)
# return None if input is neither an active player or team
def getQuickSearch(quick_input):
	player_data = statsapi.lookup_player(quick_input)
	team_data = statsapi.lookup_team(quick_input)
	res = {}
	if len(player_data) >= 1 and len(team_data) >= 1:
		res['player_data'] = player_data
		res['team_data'] = team_data
		return res
	elif len(player_data) >= 1:
		res['player_data'] = player_data
		return res
	elif len(team_data) >= 1:
		res['team_data'] = team_data
		return res
	else:
		return None

# live game functions
def setupLiveGame(gameID):
	gameData = statsapi.get(endpoint = 'game', params = {'gamePk':gameID})
	all_plays = gameData['liveData']['plays']['allPlays']
	scoring_plays = gameData['liveData']['plays']['scoringPlays']

	away = gameData['gameData']['teams']['away']['teamName']
	home = gameData['gameData']['teams']['home']['teamName']

	total_plays = len(all_plays)
	curr_play_ind = total_plays - 1 # return current play index in all_plays
	curr_AB_ind = 0					# return current AB event index
	curr_AB_events = []				# return list of events in current ongoing AB
	curr_inning_movement = []
	curr_inning_plays = [] # return list of plays in current ongoing inning
	all_events = {} 	# return map of all events that occured in game (outs, stolen bases, hits, etc.) with key being inning and value being map of events occured in that inning (with key being the half inning, value being array of events in the half-inning)
	scoring_events = []
	bases = [False] * 3 # return [first, second, third]
	AB = [0] * 3        # return [balls, strikes, outs]
	runners_scored = [] # return list of runner's ids that scored in current AB
	matchup = {} 		# current AB pitcher and batter matchup
	curr_score = [away, 0, home, 0] 	# return current score from last play, [away team, away score, home team, home score]
	linescore = {}		# return linescore info (runs, hits, errors. LOB for each inning, also has current inning info)

	if 'linescore' in gameData['liveData']:
		linescore = gameData['liveData']['linescore']

	for play in all_plays:
		inning = play['about']['inning']
		half_inning = play['about']['halfInning']
		if 'description' in play['result']:
			descr = play['result']['description']
			if inning not in all_events:
				inning_events = {}
				half_inning_events = []
				half_inning_events.append(descr)
				inning_events[half_inning] = half_inning_events
				all_events[inning] = inning_events
			elif half_inning not in all_events[inning]:
				half_inning_events = []
				half_inning_events.append(descr)
				all_events[inning][half_inning] = half_inning_events
			else: # half-inning axists in all_events map
				half_inning_events = all_events[inning][half_inning]
				half_inning_events.append(descr)

	for scoring_play_ind in scoring_plays:
		play = all_plays[int(scoring_play_ind)]
		descr = play['result']['description']
		away_score = play['result']['awayScore']
		home_score = play['result']['homeScore']
		inning = "%s %d" % (play['about']['halfInning'], play['about']['inning'])
		full_descr = inning + ": " + descr + " " + str(away_score) + " - " + str(home_score)
		scoring_events.append(full_descr)
		

	# get the inning's previous play's moevements up to the last inning's play (last innings's play has out number of 3)
	i = 1
	while total_plays > 1 and i <= total_plays and "count" in all_plays[total_plays - i] and all_plays[total_plays - i]['count']['outs'] != 3:
		if 'description' in all_plays[total_plays - i]['result']:
			curr_inning_plays.append(all_plays[total_plays - i]['result']['description'])
		curr_inning_movement.append(all_plays[total_plays- i]['runners'])
		i += 1

	if total_plays > 0:
		if 'awayScore' in all_plays[total_plays - 1]['result']:
			away_score = all_plays[total_plays - 1]['result']['awayScore']
			home_score = all_plays[total_plays - 1]['result']['homeScore']

			curr_score[1] = away_score
			curr_score[3] = home_score
		
		if 'matchup' in all_plays[total_plays - 1]:
			matchup = all_plays[total_plays - 1]['matchup']

		# if last play resulted in third out, leave base setup as empty for new inning, otherwise setup the bases based on the current inning's movement
		if "count" in all_plays[total_plays - 1] and all_plays[total_plays - 1]['count'] != 3:
			setupBases(curr_inning_movement, bases, runners_scored)

		# setup current AB count, plays, and get the current AB event index
		curr_AB_ind = setupAB(all_plays[total_plays - 1], AB, curr_AB_events)

	# return values in map for easy conversion to JSON
	res = {}
	res['curr_play_ind'] = curr_play_ind
	res['curr_AB_ind'] = curr_AB_ind
	res['curr_AB_events'] = curr_AB_events
	res['curr_inning_plays'] = curr_inning_plays
	res['all_events'] = all_events
	res['scoring_events'] = scoring_events
	res['bases'] = bases
	res['AB'] = AB
	res['runners_scored'] = runners_scored
	res['matchup'] = matchup
	res['curr_score'] = curr_score
	res['linescore'] = linescore
	return res


def setupBases(curr_inning_movement, base_status, runners_scored):
	while(curr_inning_movement):
		movement = curr_inning_movement.pop()

		# [batter's end base, 1st base runner end base, 2nd end, 3rd end]
		# null value means no player originated at that base
		end_movement = [None, None, None, None]
		for move in movement:
			origin_base = move['movement']['originBase']
			end_base = move['movement']['end']
			is_out = move['movement']['isOut']
			if origin_base == '1B':
				if is_out:
					end_movement[1] = 'out'
				elif not end_movement[1] or (end_movement[1] and (end_base > end_movement[1])):
					end_movement[1] = end_base
			elif origin_base == '2B':
				if is_out:
					end_movement[2] = 'out'
				elif not end_movement[2] or (end_movement[2] and (end_base > end_movement[2])):
					end_movement[2] = end_base
			elif origin_base == '3B':
				if is_out:
					end_movement[3] = 'out'
				elif not end_movement[3] or (end_movement[3] and (end_base > end_movement[3])):
					end_movement[3] = end_base
			else: # origin base is 'None" meaning the batter's movement
				if is_out:
					end_movement[0] = 'out'
				elif not end_movement[0] or (end_movement[0] and (end_base > end_movement[0])):
					end_movement[0] = end_base

			# if runner scored in an inning, keep track of that runner that scored
			if move['details']['isScoringEvent']:
				runners_scored.append(move['details']['runner']['id'])

		# update bases counter-clockwise: update runner on third, then second, first, batter.
		for i in range(len(end_movement) - 1, -1, -1):
			if i == 0 and end_movement[i]:
				updateBases('None', end_movement[i], base_status)
			elif i == 1 and end_movement[i]:
				updateBases('1B', end_movement[i], base_status)
			elif i == 2 and end_movement[i]:
				updateBases('2B', end_movement[i], base_status)
			elif i == 3 and end_movement[i]:
				updateBases('3B', end_movement[i], base_status)

def updateBases(origin_base, end_base, base_status):
	if end_base == '1B':
		base_status[0] = True
	elif end_base == '2B':
		base_status[1] = True
	elif end_base == '3B':
		base_status[2] = True
                        
	if origin_base == '1B':
		base_status[0] = False
	elif origin_base == '2B':
		base_status[1] = False
	elif origin_base == '3B':
		base_status[2] = False

def setupAB(currPlay, AB_status, curr_AB_events):
	currEvents = currPlay['playEvents']
	for event in currEvents:
		description = event['details']['description']
		is_pitch = event['isPitch']
		if is_pitch:
			count = event['count']
			balls = count['balls']
			strikes = count['strikes']
			
			description = "%d - %d %s : %s %0.1f mph" % (balls, strikes, description, event['details']['type']['description'], event['pitchData']['startSpeed'])
		curr_AB_events.append(description)

	if currEvents:
		currCount = currEvents[len(currEvents) - 1]['count']
		AB_status[0] = currCount['balls']
		AB_status[1] = currCount['strikes']
		AB_status[2] = currCount['outs']
        
	curr_AB_ind = len(currEvents)
	return curr_AB_ind