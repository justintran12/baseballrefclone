import unittest
from mongoDB_utils import MongoDB

class baseballStatsTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.db = MongoDB()

    def testCreateNewAndDupe(self):
        self.db.createUser("blowers")
        self.db.createUser("sims")
        self.db.createUser("blowers")
        exp = ["blowers", "sims"]
        self.assertEqual(self.db.getUsers(), exp)

        self.db.deleteAll()
        self.assertEqual(self.db.getUsers(), [])

    def testInsertDupeTeamsAndPlayersAndGet(self):
        self.db.createUser("blowers")
        self.db.createUser("sims")
        self.db.insertFav("blowers", "Jarred Kelenic", "player")
        self.db.insertFav("blowers", "Seattle Mariners", "team")
        self.db.insertFav("blowers", "Seattle Mariners", "team")
        self.db.insertFav("sims", "Ichiro Suzuki", "player")
        self.db.insertFav("sims", "Jarred Kelenic", "player")
        self.db.insertFav("blowers", "Jarred Kelenic", "player")
        self.db.insertFav("sims", "Philadelphia Phillies", "team")
        blowers_fav_teams = self.db.getFavs("blowers")["fav_teams"]
        blowers_fav_players = self.db.getFavs("blowers")["fav_players"]
        sims_fav_teams = self.db.getFavs("sims")["fav_teams"]
        sims_fav_players = self.db.getFavs("sims")["fav_players"]

        self.assertEqual(blowers_fav_teams, ["Seattle Mariners"])
        self.assertEqual(blowers_fav_players, ["Jarred Kelenic"])
        self.assertEqual(sims_fav_teams, ["Philadelphia Phillies"])
        self.assertEqual(sims_fav_players, ["Ichiro Suzuki", "Jarred Kelenic"])

        self.db.deleteAll()
        self.assertEqual(self.db.getUsers(), [])

    def testClearAndDelete(self):
        self.db.createUser("blowers")
        self.db.createUser("sims")
        self.db.insertFav("blowers", "Jarred Kelenic", "player")     
        self.db.insertFav("sims", "Ichiro Suzuki", "player")
        self.db.insertFav("blowers", "Seattle Mariners", "team")
        self.db.insertFav("sims", "Philadelphia Phillies", "team")

        self.db.clearFavs("blowers")
        self.db.clearFavs("sims")
        self.assertEqual(self.db.getUsers(), ["blowers", "sims"])
        self.assertEqual(self.db.getFavs("blowers")["fav_teams"], [])
        self.assertEqual(self.db.getFavs("blowers")["fav_players"], [])
        self.assertEqual(self.db.getFavs("sims")["fav_teams"], [])
        self.assertEqual(self.db.getFavs("sims")["fav_players"], [])

        self.db.deleteUser("blowers")
        self.assertEqual(self.db.getUsers(), ["sims"])
        self.db.deleteUser("blowers")
        self.db.deleteUser("sims")
        self.assertEqual(self.db.getUsers(), [])


if __name__ == "__main__":
    unittest.main()