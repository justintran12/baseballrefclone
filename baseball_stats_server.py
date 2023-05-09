from flask import Flask, request, jsonify, after_this_request
from flask_cors import CORS
import statsapi

app = Flask(__name__)
CORS(app)

# convert player data frpm api call into map
def getPlayerHittingStatsToMap(player_name, season_type):
	if season_type == 'career':
		player_stats_str = statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players',{'season':2022,'gameType':'W'})['people'] if x['fullName']== player_name), 'hitting', 'career')
		player_stats_arr = player_stats_str.split("Career Hitting")[1].strip().split("\n")
	else: # season
		player_stats_str = statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players',{'season':2023,'gameType':'W'})['people'] if x['fullName']== player_name), 'hitting', 'season')
		player_stats_arr = player_stats_str.split("Season Hitting")[1].strip().split("\n")

	player_stats_map = {}
	for stat in player_stats_arr:
		stat_arr = stat.split(":")
		stat_name = stat_arr[0].strip()
		stat_val = stat_arr[1].strip()
		player_stats_map[stat_name] = stat_val
		
	return player_stats_map
	
@app.route('/career', methods = ['GET'])
def getDataCareer():
	player = "Jarred Kelenic"
	player_stats_map = getPlayerHittingStatsToMap(player, 'career')
	
	'''
	@after_this_request
	def add_header (response):
		response.headers.add('Access-Control-Allow-Origin', '*')
		return response
	'''
		
	return jsonify(player_stats_map)
	
@app.route('/seasons', methods = ['GET'])
def getDataSeasons():
	player = "Jarred Kelenic"
	player_stats_map = getPlayerHittingStatsToMap(player, 'season')
	'''
	# another way to get player hitting stats for season but only works if you know player id
	#player_id = statsapi.lookup_player(player)[0]['id']
	player_id = 672284
	player_info = statsapi.player_stat_data(player_id, group="[hitting,fielding]", type="season", sportId=1)
	
	player_stats = player_info['stats']
	hitting_stats = {}

	for stat in player_stats:
		if (stat["group"] == 'hitting'):
			hitting_stats = stat["stats"]
	'''
		
		
	return jsonify(player_stats_map)

if __name__ == '__main__':
   app.run(debug = True)