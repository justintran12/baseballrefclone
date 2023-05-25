import unittest
import baseball_stats as bs

class baseballStatsTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.teams = ["Arizona Diamondbacks", "Atlanta Braves", "Baltimore Orioles", "Boston Red Sox", "Chicago White Sox", "Chicago Cubs", "Cincinnati Reds", "Cleveland Guardians", "Colorado Rockies", "Detroit Tigers", "Houston Astros", "Kansas City Royals",
                "Los Angeles Angels", "Los Angeles Dodgers", "Miami Marlins", "Milwaukee Brewers", "Minnesota Twins", "New York Yankees", "New York Mets", "Oakland Athletics", "Philadelphia Phillies", "Pittsburgh Pirates" , "San Diego Padres", 
                "San Francisco Giants", "Seattle Mariners", "St. Louis Cardinals", "Tampa Bay Rays", "Texas Rangers", "Toronto Blue Jays", "Washington Nationals"]
    def testPlayerCareer(self):
        self.assertIsNotNone(bs.getPlayerCareerStats("Jarred Kelenic", "hitting"))
        self.assertIsNotNone(bs.getPlayerCareerStats("George Kirby", "pitching"))
    def testPlayerSeason(self):
        self.assertIsNotNone(bs.getPlayerSeasonStats("Jarred Kelenic", "hitting"))
        self.assertIsNotNone(bs.getPlayerSeasonStats("George Kirby", "pitching"))
    def testLeagueLeaders(self):
        self.assertIsNotNone(bs.getLeagueLeaders())
    def testTeamLeadersData(self):
        for team_name in self.teams:
            team_id = bs.teamNameToId(team_name)
            self.assertIsNotNone(bs.getTeamLeadersData(team_id))
    def testTeamStandingsData(self):
        for team_name in self.teams:
            team_id = bs.teamNameToId(team_name)
            self.assertIsNotNone(bs.getTeamStandingsData(team_id))
    def testRosterData(self):
        for team_name in self.teams:
            team_id = bs.teamNameToId(team_name)
            self.assertIsNotNone(bs.getRosterData(team_id))


if __name__ == "__main__":
    unittest.main()