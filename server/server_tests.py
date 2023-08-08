import unittest
import baseball_stats as bs

# to run only one test: python3 server/server_tests.py baseballStatsTest.testPlayerCareer
class baseballStatsTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.teams = ["Arizona Diamondbacks", "Atlanta Braves", "Baltimore Orioles", "Boston Red Sox", "Chicago White Sox", "Chicago Cubs", "Cincinnati Reds", "Cleveland Guardians", "Colorado Rockies", "Detroit Tigers", "Houston Astros", "Kansas City Royals",
                "Los Angeles Angels", "Los Angeles Dodgers", "Miami Marlins", "Milwaukee Brewers", "Minnesota Twins", "New York Yankees", "New York Mets", "Oakland Athletics", "Philadelphia Phillies", "Pittsburgh Pirates" , "San Diego Padres", 
                "San Francisco Giants", "Seattle Mariners", "St. Louis Cardinals", "Tampa Bay Rays", "Texas Rangers", "Toronto Blue Jays", "Washington Nationals"]
    
    def testPlayerCareer(self):
        # usual case: get hitting stats for hitters and pitching stats for pitchers
        self.assertIsNotNone(bs.getPlayerCareerStats("Julio Rodriguez", "hitting"))
        self.assertIsNotNone(bs.getPlayerCareerStats("JULIO rodriguez", "hitting"))
        self.assertIsNotNone(bs.getPlayerCareerStats("George Kirby", "pitching"))
        # mismatch case: get pitching stats for hitters and hitting stats for pitchers, returns None
        self.assertIsNone(bs.getPlayerCareerStats("julio rodriguez", "pitching"))
        self.assertIsNone(bs.getPlayerCareerStats("George Kirby", "hitting"))
    
    def testPlayerSeason(self):
        self.assertIsNotNone(bs.getPlayerSeasonStats("Julio Rodriguez", "hitting"))
        self.assertIsNotNone(bs.getPlayerSeasonStats("JULIO rodriguez", "hitting"))
        self.assertIsNotNone(bs.getPlayerSeasonStats("George Kirby", "pitching"))
    
    def testLeagueLeaders(self):
        self.assertIsNotNone(bs.getLeagueLeaders())

    def testPlayerOrTeam(self):
        # If player name is unique, return "player" (case does not matter)
        self.assertEqual(bs.playerOrTeam("Julio Rodriguez"), "player")
        self.assertEqual(bs.playerOrTeam("JUlIO RodrigUEZ"), "player")
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
        self.assertIsNone(bs.playerOrTeam("hulio rodreguess"))
        self.assertIsNone(bs.playerOrTeam("juliorodriguez"))
        self.assertIsNone(bs.playerOrTeam("redsox"))
        self.assertIsNone(bs.playerOrTeam("mar iners"))
        self.assertIsNone(bs.playerOrTeam("Angels Los Angeles"))

    def testGetQuickSearch(self):
        player_only = bs.getQuickSearch("Ohtani")
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

    def testGetPlayerOrTeamSearchActive(self):
        self.assertIsNotNone(bs.getPlayerOrTeamSearch("Julio Rodriguez", "player"))
        self.assertIsNotNone(bs.getPlayerOrTeamSearch("Seattle Mariners", "team"))

    def testGetPlayerOrTeamSearchAmbiguous(self):
        self.assertTrue(len(bs.getPlayerOrTeamSearch("Julio", "player")['player_data']) > 1)
        self.assertTrue(len(bs.getPlayerOrTeamSearch("new york", "team")['team_data']) > 1)

    def testGetPlayerOrTeamSearchInactive(self):
        self.assertTrue(len(bs.getPlayerOrTeamSearch("Ichiro", "player")['player_data']) == 0)
        self.assertTrue(len(bs.getPlayerOrTeamSearch("montreal", "team")['team_data']) == 0)
        self.assertTrue(len(bs.getPlayerOrTeamSearch("thisisnotavalidinput", "player")['player_data']) == 0)

    
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
            },
            "details": {"isScoringEvent":False}
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
            },
            "details": {"isScoringEvent":False}
        }]
        ]
        bases = [False] * 3
        bs.setupBases(curr_inning_movement, bases, [])
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
            } ,
            "details": {"isScoringEvent":False}
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
            },
            "details": {"isScoringEvent":False}
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
            },
            "details": {"isScoringEvent":False}
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
            },
            "details": {"isScoringEvent":False}
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
            },
            "details": {"isScoringEvent":False}
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
            },
            "details": {"isScoringEvent":False}
        }
        ]
        ]
        bases = [False] * 3
        bs.setupBases(curr_inning_movement, bases, [])
        expected = [True] * 3
        self.assertListEqual(bases, expected)

    def testSetupBasesStolenBaseErrorDouble(self):
        curr_inning_movement = [
            [{'movement': {'originBase': '1B', 'start': '1B', 'end': '2B', 'outBase': None, 'isOut': False, 'outNumber': None}, 
            'details': {'event': 'Stolen Base 2B', 'eventType': 'stolen_base_2b', 'movementReason': 'r_stolen_base_2b', 'runner': {'id': 593160, 'fullName': 'Whit Merrifield', 'link': '/api/v1/people/593160'}, 'responsiblePitcher': None, 'isScoringEvent': False, 'rbi': False, 'earned': False, 'teamUnearned': False, 'playIndex': 1}, 
            'credits': []}, 
            {'movement': {'originBase': '1B', 'start': '2B', 'end': '3B', 'outBase': None, 'isOut': False, 'outNumber': None}, 
            'details': {'event': 'Error', 'eventType': 'error', 'movementReason': 'r_adv_play', 'runner': {'id': 593160, 'fullName': 'Whit Merrifield', 'link': '/api/v1/people/593160'}, 'responsiblePitcher': None, 'isScoringEvent': False, 'rbi': False, 'earned': False, 'teamUnearned': False, 'playIndex': 1}, 
            'credits': [{'player': {'id': 642136, 'link': '/api/v1/people/642136'}, 'position': {'code': '2', 'name': 'Catcher', 'type': 'Catcher', 'abbreviation': 'C'}, 'credit': 'f_throwing_error'}]}, 
            {'movement': {'originBase': None, 'start': None, 'end': '2B', 'outBase': None, 'isOut': False, 'outNumber': None}, 
            'details': {'event': 'Double', 'eventType': 'double', 'movementReason': None, 'runner': {'id': 666182, 'fullName': 'Bo Bichette', 'link': '/api/v1/people/666182'}, 'responsiblePitcher': None, 'isScoringEvent': False, 'rbi': False, 'earned': False, 'teamUnearned': False, 'playIndex': 4}, 
            'credits': [{'player': {'id': 621493, 'link': '/api/v1/people/621493'}, 'position': {'code': '7', 'name': 'Outfielder', 'type': 'Outfielder', 'abbreviation': 'LF'}, 'credit': 'f_fielded_ball'}]}, 
            {'movement': {'originBase': '3B', 'start': '3B', 'end': 'score', 'outBase': None, 'isOut': False, 'outNumber': None}, 
            'details': {'event': 'Double', 'eventType': 'double', 'movementReason': 'r_adv_play', 'runner': {'id': 593160, 'fullName': 'Whit Merrifield', 'link': '/api/v1/people/593160'}, 'responsiblePitcher': {'id': 608337, 'link': '/api/v1/people/608337'}, 'isScoringEvent': True, 'rbi': True, 'earned': True, 'teamUnearned': False, 'playIndex': 4}, 'credits': []}],
            [{'movement': {'originBase': None, 'start': None, 'end': '1B', 'outBase': None, 'isOut': False, 'outNumber': None}, 
            'details': {'event': 'Single', 'eventType': 'single', 'movementReason': None, 'runner': {'id': 593160, 'fullName': 'Whit Merrifield', 'link': '/api/v1/people/593160'}, 'responsiblePitcher': None, 'isScoringEvent': False, 'rbi': False, 'earned': False, 'teamUnearned': False, 'playIndex': 3}, 
            'credits': [{'player': {'id': 621493, 'link': '/api/v1/people/621493'}, 'position': {'code': '7', 'name': 'Outfielder', 'type': 'Outfielder', 'abbreviation': 'LF'}, 'credit': 'f_fielded_ball'}]}]
        ]

        bases = [False] * 3
        bs.setupBases(curr_inning_movement, bases, [])
        expected = [False, True, False]
        self.assertListEqual(bases, expected)

    def testSetupAB(self):
        AB = [0] * 3
        curr_AB_events = []
        currPlay = {"playEvents": [
        {
            "details": {
                "description": "Ball",
                "type": {
                    "code": "KC",
                    "description": "Knuckle Curve"
                }
            },
            "count": {
                "balls": 1,
                "strikes": 0,
                "outs": 1
            },
            "pitchData": {
                "startSpeed": 85.6,
                "endSpeed": 79.3
            },
            "isPitch": True
        }, 
        {
            "details": {
                "description": "Batter Timeout",
            },
            "count": {
                "balls": 1,
                "strikes": 0,
                "outs": 1
            },
            "isPitch": False   
        }
        ]
        }
        bs.setupAB(currPlay, AB, curr_AB_events)
        
        expected_AB = [1,0,1]
        expected_AB_events = ["1 - 0 Ball : Knuckle Curve 85.6 mph", "Batter Timeout"]
        self.assertListEqual(AB, expected_AB)
        self.assertListEqual(curr_AB_events, expected_AB_events)

    
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