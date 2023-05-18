from flask import Flask, request, jsonify, after_this_request
from flask_cors import CORS
import statsapi

app = Flask(__name__)
CORS(app)

# convert player data frpm api call into map
def getPlayerCareerStats(player_name, player_type):
	id = next(x['id'] for x in statsapi.get('sports_players',{'season':2023,'gameType':'W'})['people'] if x['fullName']== player_name)
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
	id = next(x['id'] for x in statsapi.get('sports_players',{'season':2023,'gameType':'W'})['people'] if x['fullName']== player_name)

	stats_seasons_map = {}
	for season_data in statsapi.player_stat_data(id, group=player_type, type="yearByYear", sportId=1)['stats']:
		year = season_data['season']
		stats_seasons_map[year] = season_data['stats']
	
	return stats_seasons_map
	
@app.route('/career', methods = ['GET'])
def getDataCareer():
	player_user_input = request.values.get('player_name')
	player_user_type = request.values.get('player_type')
	player_stats_map = getPlayerCareerStats(player_user_input, player_user_type)
		
	return jsonify(player_stats_map)
	
@app.route('/seasons', methods = ['GET'])
def getDataSeasons():
	player_user_input = request.values.get('player_name')
	player_user_type = request.values.get('player_type')
	player_stats_map = getPlayerSeasonStats(player_user_input, player_user_type)
		
	return jsonify(player_stats_map)


if __name__ == '__main__':
   app.run(debug = True)