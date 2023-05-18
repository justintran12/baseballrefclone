from flask import Flask, request, jsonify, after_this_request
from flask_cors import CORS
import statsapi

app = Flask(__name__)
CORS(app)

# convert player data frpm api call into map
def getPlayerCareerHittingStats(player_name):
	id = next(x['id'] for x in statsapi.get('sports_players',{'season':2023,'gameType':'W'})['people'] if x['fullName']== player_name)
	player_stats_str = statsapi.player_stats(id, 'hitting', 'career')
	player_stats_arr = player_stats_str.split("Career Hitting")[1].strip().split("\n")

	player_stats_map = {}
	for stat in player_stats_arr:
		stat_arr = stat.split(":")
		stat_name = stat_arr[0].strip()
		stat_val = stat_arr[1].strip()
		player_stats_map[stat_name] = stat_val
		
	return player_stats_map

def getPlayerSeasonHittingStats(player_name):
	id = next(x['id'] for x in statsapi.get('sports_players',{'season':2023,'gameType':'W'})['people'] if x['fullName']== player_name)

	stats_seasons_map = {}
	for season_data in statsapi.player_stat_data(id, group="hitting", type="yearByYear", sportId=1)['stats']:
		year = season_data['season']
		stats_seasons_map[year] = season_data['stats']
	
	return stats_seasons_map
	
@app.route('/career', methods = ['GET'])
def getDataCareer():
	player_user_input = request.values.get('player_name')
	player_stats_map = getPlayerCareerHittingStats(player_user_input)
		
	return jsonify(player_stats_map)
	
@app.route('/seasons', methods = ['GET'])
def getDataSeasons():
	player_user_input = request.values.get('player_name')
	player_stats_map = getPlayerSeasonHittingStats(player_user_input)
		
	return jsonify(player_stats_map)


if __name__ == '__main__':
   app.run(debug = True)