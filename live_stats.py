import statsapi

class Game:

    def __init__(self):
        self.gameID = 0
        self.first = False
        self.second = False
        self.third = False
        self.plays = []
        self.curr_inning_plays = []
        self.curr_play_ind = 0

    def setup(self, gameID):
        self.gameID = gameID
        curr_inning_movement = []

        all_plays = statsapi.get(endpoint = 'game', params = {'gamePk':gameID})['liveData']['plays']['allPlays']

        #inning_plays = []
        for play in all_plays:
            self.plays.append(play['result'])
            '''
            if (play['runners'][len(play['runners']) - 1]['movement']['outNumber'] == 3):
                self.plays.append(inning_plays)
                inning_plays = []
            '''

        total_plays = len(all_plays)
        last_play_runners = []
        if total_plays > 0:
            last_play_runners = all_plays[total_plays - 1]['runners']
        # need to handle empty runners list (when AB is ongoing) and double plays or any plays that have multiple outs (need to check the last movement in the play for the right out number)
        if total_plays > 0 and last_play_runners and last_play_runners[len(last_play_runners) - 1]['movement']['outNumber'] != 3:
            curr_inning_movement.append(last_play_runners)
        elif total_plays > 0 and last_play_runners and last_play_runners[len(last_play_runners) - 1]['movement']['outNumber'] == 3:
            self.curr_inning_plays.append(all_plays[total_plays - 1]['result'])

        i = 2
        while total_plays > 0 and all_plays[total_plays - i]['runners'][len(all_plays[total_plays - i]['runners']) - 1]['movement']['outNumber'] != 3:
            self.curr_inning_plays.append(all_plays[total_plays - i]['result'])
            curr_inning_movement.append(all_plays[total_plays- i]['runners'])
            i += 1
        
        self.curr_play_ind = total_plays - 1
        self.setupBases(curr_inning_movement)

    def setupBases(self, curr_inning_movement):
        while(curr_inning_movement):
            origin_seen = set()
            movement = curr_inning_movement.pop()
            print(movement)

            # batter's movement comes first in movement list
            # then player on 3rd's movement, then player on 2nd, then player on 1st
            # process player movements in order: 3rd, 2nd, 1at, batter
            for i in range(len(movement)):
                move = movement[i]
                is_out = move['movement']['isOut']
                origin_base = move['movement']['originBase']
                if origin_base:
                    end_base = move['movement']['end']
                    if not is_out and origin_base not in origin_seen:
                        if end_base == '1B':
                            self.first = True
                        elif end_base == '2B':
                            self.second = True
                        elif end_base == '3B':
                            self.third = True
                        
                        if origin_base == '1B':
                            self.first = False
                        elif origin_base == '2B':
                            self.second = False
                        elif origin_base == '3B':
                            self.third = False

                        origin_seen.add(origin_base)

            for i in range(len(movement)):
                move = movement[i]
                is_out = move['movement']['isOut']
                origin_base = move['movement']['originBase']
                if not origin_base:
                    end_base = move['movement']['end']
                    if not is_out and origin_base not in origin_seen:
                        if end_base == '1B':
                            self.first = True
                        elif end_base == '2B':
                            self.second = True
                        elif end_base == '3B':
                            self.third = True
                        
                        if origin_base == '1B':
                            self.first = False
                        elif origin_base == '2B':
                            self.second = False
                        elif origin_base == '3B':
                            self.third = False

                        origin_seen.add(origin_base)


    def update(self):
        all_plays = statsapi.get(endpoint = 'game', params = {'gamePk':self.gameID})['liveData']['plays']['allPlays']


    

game = Game()
game.setup(717719)
print(game.first)
print(game.second)
print(game.third)
print(game.curr_inning_plays)
'''
for play in game.plays:
    print(play)
'''
    