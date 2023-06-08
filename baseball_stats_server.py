from flask import Flask, request, jsonify, after_this_request
from flask_cors import CORS
import baseball_stats as bs
from mongoDB_utils import MongoDB

app = Flask(__name__)
CORS(app)

# initialize database
db = MongoDB()

# endpoints exposed

# endpoints to get player data:
# input player name in body data, ex: {'player_name' : 'Ichiro Suzuki'}

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

# no input body data needed
# return map with keys: stat type, values: map of leader data (keys: player name, player team, player rank)
@app.route('/leaders', methods = ['GET'])
def getDataLeaders():
	return jsonify(bs.getLeagueLeaders())

# endpoints to get team data:
# input team name in body data, ex: {'team_name' : 'Seattle Mariners'}

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

# endpoints to get/manipulate user data in database:

# input body example: {'new_username' : 'bob', 'new_password': 'bob_rules'}
# if user already exists in database, createUser does not create the new user, return created = false
@app.route('/createUser', methods = ['POST'])
def createNewUser():
	new_username = request.values.get('new_username')
	new_password = request.values.get('new_password')
	resp = db.createUser(new_username, new_password)

	return {'created' : 'true'} if resp else {'created' : 'false'}

@app.route('/validateUser', methods = ['POST'])
def validateUser():
	username = request.values.get('username')
	password = request.values.get('password')
	resp = db.validateUser(username, password)

	return {'valid' : 'true'} if resp else {'valid' : 'false'}

# input body example: {'username' : 'bob'}
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

# input body example for players: {'fav_name' : 'Jarred Kelenic', 'type' : 'player', 'username' : 'bob'}
#					 for teams:	  {'fav_name' : 'Seattle Mariners', 'type' : 'team', 'username' : 'bob'}
# inputs with type other than 'player' or 'team' will result in resp = False from insert function, nothing will be inserted into database
# if favorite already exists in database, insertFav does not insert the favorite, return inserted = false
@app.route('/insertUserFavs', methods = ['POST'])
def insertUserFavs():
	fav_name = request.values.get('fav_name')
	fav_type = request.values.get('type')
	username = request.values.get('username')

	resp = db.insertFav(username, fav_name, fav_type)

	return {'inserted' : 'true'} if resp else {'inserted' : 'false'}

# input body example: {'fav' : 'Aaron Judge', 'username' : 'bob'}
@app.route('/deleteFav', methods = ['POST'])
def deleteFav():
	fav = request.values.get('fav')
	username = request.values.get('username')

	resp = db.deleteFav(fav, username)
	return jsonify(success=True) if resp else jsonify(success=False)

if __name__ == '__main__':
   app.run(debug = True)