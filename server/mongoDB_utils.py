import pymongo
from pymongo import MongoClient
import hashlib

class MongoDB:
    def __init__(self):
        client = MongoClient()
        self.db = client["user_favorites"]
        self.favorites = self.db["favorites"]
        self.salt = "bjt"

    # assume createUser only called when username does not already exist in collection, but just in case do not create a duplicate username document. Return true if created a new user, false if user already exists.
    def createUser(self, username, password):
        # Adding salt at the last of the password
        dataBase_password = password + self.salt
        # Encoding the password
        hashed = hashlib.md5(dataBase_password.encode())
        encoded_pw = hashed.hexdigest()
        
        if not self.getFavs(username):
            user_favs = {"user": username,
                        "password": encoded_pw,
                        "fav_teams": [],
                        "fav_players": []}
            self.favorites.insert_one(user_favs)
            return True
        return False

    # returns false if username does not exist in database or given password is incorrect for the given username, otherwise if correct password for existing username is given return true
    def validateUser(self, username, password):
        # Adding salt at the last of the password
        dataBase_password = password + self.salt
        # Encoding the password
        hashed = hashlib.md5(dataBase_password.encode())
        input_pw = hashed.hexdigest()

        fav_doc = self.getFavs(username)

        if fav_doc:
            correct_pw = fav_doc["password"]
            if input_pw == correct_pw:
                return True
            else:
                return False
        else: 
            return False

    # assume when insertFav is called, the username exists in the collection. Duplicate favorites will not be added and false is returned. If favorite is successfully added, true is returned.
    # only insert a favorite player or team, other types are not valid and function will return false without inserting anything
    def insertFav(self, username, fav, favType):
        fav_doc = self.getFavs(username)
        if favType == "player":
            fav_type = "fav_players"
        elif favType == 'team':
            fav_type = "fav_teams"
        else: 
            return False

        fav_list = fav_doc[fav_type]
        if fav not in fav_list:
            fav_list.append(fav)
            filter = { "user" : username}
            new_favs = { "$set": { fav_type : fav_list} }
            self.favorites.update_one(filter, new_favs)
            return True
        return False

    # returns None if username not in collection
    def getFavs(self, username):
        return self.favorites.find_one({"user": username})

    # return list of all users in collection
    def getUsers(self):
        cursor = self.favorites.find({})
        users = []
        for document in cursor:
            users.append(document['user'])
        return users

    # keep username in collection, but clear all favorites
    def clearFavs(self, username):
        filter = { "user" : username}
        reset_favs = { "$set": { "fav_players" : [], "fav_teams" : []} }
        self.favorites.update_one(filter, reset_favs)

    # delete user if it exists in collection
    def deleteUser(self, username):
        if self.getFavs(username):
            self.favorites.delete_one({"user" : username})
    
    # delete all users
    def deleteAll(self):
        self.favorites.delete_many({})

    # delete a favorite team or player, only called when the x button associated with that favorite is clicked, so favorite is guaranteed to be in database
    # but if calling API from elsewhere, if favorite not in database, returns False and does not update database
    def deleteFav(self, fav, username):
        fav_doc = self.getFavs(username)
        if fav_doc == None:
            return False

        fav_players = fav_doc["fav_players"]
        fav_teams = fav_doc["fav_teams"]
        filter = { "user" : username}

        if fav in fav_players:
            fav_players.remove(fav)
            new_favs = { "$set": { "fav_players" : fav_players} }
        elif fav in fav_teams:
            fav_teams.remove(fav)
            new_favs = { "$set": { "fav_teams" : fav_teams} }
        else:
            return False

        self.favorites.update_one(filter, new_favs)
        return True

#mongo = MongoDB()
#mongo.clearFavs("justin")