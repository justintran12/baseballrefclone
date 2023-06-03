from flask import Flask, request, jsonify, after_this_request
from flask_cors import CORS
import baseball_stats as bs
from mongoDB_utils import MongoDB

app = Flask(__name__)
CORS(app)

# initialize database
db = MongoDB()

# endpoints exposed

# return map with keys: player stat types and the player type (pitcher/hitter), values: stat values
@app.route('/career', methods = ['GET'])
def getDataCareer():
	player_user_input = request.values.get('player_name')
	player_user_type = bs.getPlayerType(player_user_input)
	player_stats_map = bs.getPlayerCareerStats(player_user_input, player_user_type)
	player_stats_map['type'] = player_user_type
		
	return jsonify(player_stats_map)
	
# return structure same as getDataCareer()
@app.route('/seasons', methods = ['GET'])
def getDataSeasons():
	player_user_input = request.values.get('player_name')
	player_user_type = bs.getPlayerType(player_user_input)
	player_stats_map = bs.getPlayerSeasonStats(player_user_input, player_user_type)
	player_stats_map['type'] = player_user_type
		
	return jsonify(player_stats_map)

# return map with keys: stat type, values: map of leader data (keys: player name, player team, player rank)
@app.route('/leaders', methods = ['GET'])
def getDataLeaders():
	return jsonify(bs.getLeagueLeaders())

# return map with keys: player name, values: map of the player's statistics for the current season (keys: year, name, position, number, etc.)
@app.route('/roster', methods = ['GET'])
def getTeamRoster():
	team_name = request.values.get('team_name')
	team_id = bs.teamNameToId(team_name)
	roster_map = bs.getRosterData(team_id)

	return jsonify(roster_map)

# return map with keys: team name, values: map of team stats and division stats (keys: rank, GB, W, L. wc_rank, wc_gb)
@app.route('/teamStandings', methods = ['GET'])
def getTeamStandings():
	team_name = request.values.get('team_name')
	team_id = bs.teamNameToId(team_name)
	div_standings_map = bs.getTeamStandingsData(team_id)

	return jsonify(div_standings_map)

# return structure similar to getDataLeaders()
@app.route('/teamLeaders', methods = ['GET'])
def getTeamLeaders():
	team_name = request.values.get('team_name')
	team_id = bs.teamNameToId(team_name)
	team_leaders_map = bs.getTeamLeadersData(team_id)

	return jsonify(team_leaders_map)

# if user already exists in database, createUser does not create the new user, return created = false
@app.route('/createUser', methods = ['POST'])
def createNewUser():
	new_username = request.values.get('new_username')
	resp = db.createUser(new_username)

	return {'created' : 'true'} if resp else {'created' : 'false'}

# getFavs will return None if user does not exist in database
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

# if favorite already exists in database, insertFav does not insert the favorite, return inserted = false
@app.route('/insertUserFavs', methods = ['POST'])
def insertUserFavs():
	fav_name = request.values.get('fav_name')
	fav_type = request.values.get('type')
	username = request.values.get('username')

	resp = db.insertFav(username, fav_name, fav_type)

	return {'inserted' : 'true'} if resp else {'inserted' : 'false'}

@app.route('/deleteFav', methods = ['POST'])
def deleteFav():
	fav = request.values.get('fav')
	username = request.values.get('username')

	db.deleteFav(fav, username)
	return jsonify(success=True)

if __name__ == '__main__':
   app.run(debug = True)