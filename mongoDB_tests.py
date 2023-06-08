import unittest
from mongoDB_utils import MongoDB

class baseballStatsTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.db = MongoDB()

    def testCreateNewAndDupeUsers(self):
        self.assertTrue(self.db.createUser("blowers", "injured"))
        self.assertTrue(self.db.createUser("sims", "delivery"))
        self.assertFalse(self.db.createUser("blowers", "veryinjured"))
        exp = ["blowers", "sims"]
        self.assertEqual(self.db.getUsers(), exp)

        self.db.deleteAll()
        self.assertEqual(self.db.getUsers(), [])

    def testInsertDupeTeamsAndPlayersAndGet(self):
        self.assertTrue(self.db.createUser("blowers", "concussed"))
        self.assertTrue(self.db.createUser("sims", "comp"))
        self.assertTrue(self.db.insertFav("blowers", "Jarred Kelenic", "player"))
        self.assertTrue(self.db.insertFav("blowers", "Seattle Mariners", "team"))
        self.assertFalse(self.db.insertFav("blowers", "Seattle Mariners", "team"))
        self.assertTrue(self.db.insertFav("sims", "Ichiro Suzuki", "player"))
        self.assertTrue(self.db.insertFav("sims", "Jarred Kelenic", "player"))
        self.assertFalse( self.db.insertFav("blowers", "Jarred Kelenic", "player"))
        self.assertTrue(self.db.insertFav("sims", "Philadelphia Phillies", "team"))

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

    def testClearFavsAndDeleteUser(self):
        self.db.createUser("blowers", "EQC")
        self.db.createUser("sims", "achilles")
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

    def testCreateUserAndValidateUser(self):
        self.assertTrue(self.db.createUser("blowers", "bronchitis"))
        self.assertTrue(self.db.validateUser("blowers", "bronchitis"))
        self.assertFalse(self.db.validateUser("blowers", "healthy"))
        self.assertFalse(self.db.validateUser("sims", "bronchitis"))
        
        self.db.deleteAll()
        self.assertEqual(self.db.getUsers(), [])


if __name__ == "__main__":
    unittest.main()