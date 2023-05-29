from flask import Flask, request, jsonify, after_this_request
from flask_cors import CORS
import baseball_stats as bs
from mongoDB_utils import MongoDB

app = Flask(__name__)
CORS(app)

db = MongoDB()

# endpoints exposed
@app.route('/career', methods = ['GET'])
def getDataCareer():
	player_user_input = request.values.get('player_name')
	player_user_type = request.values.get('player_type')
	player_stats_map = bs.getPlayerCareerStats(player_user_input, player_user_type)
		
	return jsonify(player_stats_map)
	
@app.route('/seasons', methods = ['GET'])
def getDataSeasons():
	player_user_input = request.values.get('player_name')
	player_user_type = request.values.get('player_type')
	player_stats_map = bs.getPlayerSeasonStats(player_user_input, player_user_type)
		
	return jsonify(player_stats_map)

@app.route('/leaders', methods = ['GET'])
def getDataLeaders():
	return jsonify(bs.getLeagueLeaders())

@app.route('/roster', methods = ['GET'])
def getTeamRoster():
	team_name = request.values.get('team_name')
	team_id = bs.teamNameToId(team_name)
	roster_map = bs.getRosterData(team_id)

	return jsonify(roster_map)

@app.route('/teamStandings', methods = ['GET'])
def getTeamStandings():
	team_name = request.values.get('team_name')
	team_id = bs.teamNameToId(team_name)
	div_standings_map = bs.getTeamStandingsData(team_id)

	return jsonify(div_standings_map)


@app.route('/teamLeaders', methods = ['GET'])
def getTeamLeaders():
	team_name = request.values.get('team_name')
	team_id = bs.teamNameToId(team_name)
	team_leaders_map = bs.getTeamLeadersData(team_id)

	return jsonify(team_leaders_map)

@app.route('/createUser', methods = ['POST'])
def createNewUser():
	new_username = request.values.get('new_username')
	resp = db.createUser(new_username)

	return {'created' : 'true'} if resp else {'created' : 'false'}

@app.route('/getUserFavs', methods = ['GET'])
def getUserFavs():
	username = request.values.get('username')
	user_doc = db.getFavs(username)

	if user_doc is None:
		return {'found' : 'false'}
	else:
		user_favs = {}
		user_favs['found'] = 'true'
		user_favs['fav_players'] = user_doc['fav_players']
		user_favs['fav_teams'] = user_doc['fav_teams']
		return jsonify(user_favs)

@app.route('/insertUserFavs', methods = ['POST'])
def insertUserFavs():
	fav_name = request.values.get('fav_name')
	fav_type = request.values.get('type')
	username = request.values.get('username')

	resp = db.insertFav(username, fav_name, fav_type)

	return {'inserted' : 'true'} if resp else {'inserted' : 'false'}


if __name__ == '__main__':
   app.run(debug = True)