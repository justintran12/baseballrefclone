import unittest
import baseball_stats as bs

class baseballStatsTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.teams = ["Arizona Diamondbacks", "Atlanta Braves", "Baltimore Orioles", "Boston Red Sox", "Chicago White Sox", "Chicago Cubs", "Cincinnati Reds", "Cleveland Guardians", "Colorado Rockies", "Detroit Tigers", "Houston Astros", "Kansas City Royals",
                "Los Angeles Angels", "Los Angeles Dodgers", "Miami Marlins", "Milwaukee Brewers", "Minnesota Twins", "New York Yankees", "New York Mets", "Oakland Athletics", "Philadelphia Phillies", "Pittsburgh Pirates" , "San Diego Padres", 
                "San Francisco Giants", "Seattle Mariners", "St. Louis Cardinals", "Tampa Bay Rays", "Texas Rangers", "Toronto Blue Jays", "Washington Nationals"]
    
    def testPlayerCareer(self):
        # usual case: get hitting stats for hitters and pitching stats for pitchers
        self.assertIsNotNone(bs.getPlayerCareerStats("Jarred Kelenic", "hitting"))
        self.assertIsNotNone(bs.getPlayerCareerStats("JaRRed KELEnic", "hitting"))
        self.assertIsNotNone(bs.getPlayerCareerStats("George Kirby", "pitching"))
        # mismatch case: get pitching stats for hitters and hitting stats for pitchers, returns None
        self.assertIsNone(bs.getPlayerCareerStats("Jarred Kelenic", "pitching"))
        self.assertIsNone(bs.getPlayerCareerStats("George Kirby", "hitting"))
    
    def testPlayerSeason(self):
        self.assertIsNotNone(bs.getPlayerSeasonStats("Jarred Kelenic", "hitting"))
        self.assertIsNotNone(bs.getPlayerSeasonStats("George Kirby", "pitching"))
    
    def testLeagueLeaders(self):
        self.assertIsNotNone(bs.getLeagueLeaders())

    def testPlayerOrTeam(self):
        # If player name is unique, return "player" (case does not matter)
        self.assertEqual(bs.playerOrTeam("Jarred Kelenic"), "player")
        self.assertEqual(bs.playerOrTeam("JARRED kelenIC"), "player")
        # apparently only one active player in MLB with first or last name "Jarred" with 2 r's. There is a Jared Walsh (one r).
        self.assertEqual(bs.playerOrTeam("jarred"), "player")
        # if team name is unique, return "team"
        self.assertEqual(bs.playerOrTeam("Seattle Mariners"), "team")
        self.assertEqual(bs.playerOrTeam("SeATTle MariNERs"), "team")
        self.assertEqual(bs.playerOrTeam("seattle"), "team")
        self.assertEqual(bs.playerOrTeam("mariners"), "team")
        # if input name is ambiguous or is neither an active player or team (spelling, spacing, order (city then team name) matters), return None
        # ambiguous
        self.assertIsNone(bs.playerOrTeam("rand"))
        self.assertIsNone(bs.playerOrTeam("Los Angeles"))
        # misspelled or missing space
        self.assertIsNone(bs.playerOrTeam("jarred kelnic"))
        self.assertIsNone(bs.playerOrTeam("jarredkelenic"))
        self.assertIsNone(bs.playerOrTeam("redsox"))
        self.assertIsNone(bs.playerOrTeam("mar iners"))
        self.assertIsNone(bs.playerOrTeam("Angels Los Angeles"))

    def testGetQuickSearch(self):
        player_only = bs.getQuickSearch("kelenic")
        team_only = bs.getQuickSearch("mariners")
        both = bs.getQuickSearch("sea")
        nothing = bs.getQuickSearch("dfadfere")

        self.assertIn("player_data", player_only)
        self.assertNotIn("team_data", player_only)

        self.assertIn("team_data", team_only)
        self.assertNotIn("player_data", team_only)

        self.assertIn("player_data", both)
        self.assertIn("team_data", both)

        self.assertIsNone(nothing)

    
    # test live game functions
    def testSetupBasesAllOuts(self):
        curr_inning_movement = [
        [{
            "movement": 
            {
                "originBase": None,
                "start": None,
                "end": None,
                "outBase": "1B",
                "isOut": True,
                "outNumber": 2
            }
        }],
        [{
            "movement": 
            {
                "originBase": None,
                "start": None,
                "end": None,
                "outBase": "1B",
                "isOut": True,
                "outNumber": 1
            }
        }]
        ]
        bases = [False] * 3
        bs.setupBases(curr_inning_movement, bases)
        expected = [False] * 3
        self.assertListEqual(bases, expected)

    def testSetupBases3Singles(self):
        curr_inning_movement = [
        [{
            "movement": 
            {
                "originBase": None,
                "start": None,
                "end": "1B",
                "outBase": None,
                "isOut": False,
                "outNumber": 0
            }
        }],
        [
        {
            "movement": 
            {
                "originBase": None,
                "start": None,
                "end": "1B",
                "outBase": None,
                "isOut": False,
                "outNumber": 0
            }
        },
        {
            "movement":            
            {
                "originBase": "1B",
                "start": "1B",
                "end": "2B",
                "outBase": None,
                "isOut": False,
                "outNumber": 0
            }
        }
        ],
        [
        {
            "movement": 
            {
                "originBase": None,
                "start": None,
                "end": "1B",
                "outBase": None,
                "isOut": False,
                "outNumber": 0
            }
        },
        {
            "movement":            
            {
                "originBase": "1B",
                "start": "1B",
                "end": "2B",
                "outBase": None,
                "isOut": False,
                "outNumber": 0
            }
        },
        {
            "movement":            
            {
                "originBase": "2B",
                "start": "2B",
                "end": "3B",
                "outBase": None,
                "isOut": False,
                "outNumber": 0
            }
        }
        ]
        ]
        bases = [False] * 3
        bs.setupBases(curr_inning_movement, bases)
        expected = [True] * 3
        self.assertListEqual(bases, expected)
    
    '''
    # takes long time, tests data for all teams
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
    '''



if __name__ == "__main__":
    unittest.main()