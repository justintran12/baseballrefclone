import pymongo
from pymongo import MongoClient

class MongoDB:
    def __init__(self):
        client = MongoClient()
        self.db = client["user_favorites"]
        self.favorites = self.db["favorites"]

    # assume createUser only called when username does not already exist in collection, but just in case do not create a duplicate username document. Return true if created a new user.
    def createUser(self, username):
        if not self.getFavs(username):
            user_favs = {"user": username,
                        "fav_teams": [],
                        "fav_players": []}
            self.favorites.insert_one(user_favs)
            return True
        return False

    # assume when insertFav is called, the username exists in the collection. Duplicate favorites will not be added and false is returned. If favorite is successfully added, true is returned.
    def insertFav(self, username, fav, favType):
        fav_doc = self.getFavs(username)
        fav_type = "fav_players" if favType == "player" else "fav_teams"
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

#mongo = MongoDB()
#mongo.clearFavs("justin")