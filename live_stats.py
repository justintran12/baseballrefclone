import statsapi
import time

class Game:

    def __init__(self):
        self.gameID = 0
        self.first = False
        self.second = False
        self.third = False
        self.balls = 0
        self.strikes = 0
        self.outs = 0
        self.plays = []
        self.curr_inning_plays = []
        self.curr_AB_events = []
        self.curr_AB_movement = set()
        self.curr_play_ind = 0
        self.curr_AB_ind = 0
        

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
        '''
        last_play_runners = []
        if total_plays > 0:
            last_play_runners = all_plays[total_plays - 1]['runners']
        # need to handle empty runners list (when AB is ongoing) and double plays or any plays that have multiple outs (need to check the last movement in the play for the right out number)
        # if last play runners list is empty or last play's last out is 3, no need to setup the bases, since a new inning is starting/about to start
        if total_plays > 0 and last_play_runners and last_play_runners[len(last_play_runners) - 1]['movement']['outNumber'] != 3:
            curr_inning_movement.append(last_play_runners)

        '''

        # get the inning's previous play's moevements up to the last inning's play (last innings's play has out number of 3)
        i = 1
        while total_plays > 1 and "count" in all_plays[total_plays - i] and all_plays[total_plays - i]['count']['outs'] != 3:
            self.curr_inning_plays.append(all_plays[total_plays - i]['result'])
            curr_inning_movement.append(all_plays[total_plays- i]['runners'])
            i += 1
        
        self.curr_play_ind = total_plays - 1

        # if last play resulted in third out, reset the bases for new inning, otherwise setup the bases based on the current inning's movement
        if total_plays > 0 and "count" in all_plays[total_plays - 1] and all_plays[total_plays - 1]['count'] != 3:
            self.setupBases(curr_inning_movement)

        self.setupAB(all_plays[total_plays - 1])

    def setupBases(self, curr_inning_movement):
        while(curr_inning_movement):
            movement = curr_inning_movement.pop()

            # [batter's end base, 1st base runner end base, 2nd end, 3rd end]
            # null value means no player originated at that base
            end_movement = [None, None, None, None]
            for move in movement:
                origin_base = move['movement']['originBase']
                end_base = move['movement']['end']
                is_out = move['movement']['isOut']
                if origin_base == '1B':
                    if is_out:
                        end_movement[1] = 'out'
                    elif not end_movement[1] or (end_movement[1] and (end_base > end_movement[1])):
                        end_movement[1] = end_base
                elif origin_base == '2B':
                    if is_out:
                        end_movement[2] = 'out'
                    elif not end_movement[2] or (end_movement[2] and (end_base > end_movement[2])):
                        end_movement[2] = end_base
                elif origin_base == '3B':
                    if is_out:
                        end_movement[3] = 'out'
                    elif not end_movement[3] or (end_movement[3] and (end_base > end_movement[3])):
                        end_movement[3] = end_base
                else: # origin base is 'None" meaning the batter's movement
                    if is_out:
                        end_movement[0] = 'out'
                    elif not end_movement[0] or (end_movement[0] and (end_base > end_movement[0])):
                        end_movement[0] = end_base

            # update bases counter-clockwise: update runner on third, then second, first, batter.
            for i in range(len(end_movement) - 1, -1, -1):
                if i == 0 and end_movement[i]:
                    self.updateBases('None', end_movement[i])
                elif i == 1 and end_movement[i]:
                    self.updateBases('1B', end_movement[i])
                elif i == 2 and end_movement[i]:
                    self.updateBases('2B', end_movement[i])
                elif i == 3 and end_movement[i]:
                    self.updateBases('3B', end_movement[i])

    def setupAB(self, currPlay):
        currEvents = currPlay['playEvents']
        currAB_events = []
        for event in currEvents:
            currAB_events.append(event['details']['description'])
        self.curr_AB_events = currAB_events

        if currEvents:
            currCount = currEvents[len(currEvents) - 1]['count']
            self.balls = currCount['balls']
            self.strikes = currCount['strikes']
            self.outs = currCount['outs']
        
        self.curr_AB_ind = len(currEvents)

    def resetBases(self):
        self.first = False
        self.second = False
        self.third = False

    def updateBases(self, origin_base, end_base):
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

    def update(self):
        all_plays = statsapi.get(endpoint = 'game', params = {'gamePk':self.gameID})['liveData']['plays']['allPlays']

        print(self.curr_play_ind)
        print(len(all_plays))
        # sometimes len(all_plays) gets decremented by 1 for some reason, if that happens just wait for it to fix itself in next update
        if self.curr_play_ind < len(all_plays):

            # if current play has base movements, get the last movement's out if the movement resulted in an out, otherwise current outs is not changed
            if all_plays[self.curr_play_ind]['runners']:
                #print(all_plays[self.curr_play_ind]['runners'][len(all_plays[self.curr_play_ind]['runners']) - 1])
                if all_plays[self.curr_play_ind]['runners'][len(all_plays[self.curr_play_ind]['runners']) - 1]['movement']['isOut']:
                    self.outs = all_plays[self.curr_play_ind]['runners'][len(all_plays[self.curr_play_ind]['runners']) - 1]['movement']['outNumber']
            
            # update bases based on any new movements in AB or result of AB
            # can't assume the order of moves in 'runners' list, could be the runner on third's movement first or the runner on third's movement last
            new_movement = []
            inning_movement = []
            for move in all_plays[self.curr_play_ind]['runners']:
                print(move)
                move_str = str(move)
                if move_str not in self.curr_AB_movement:
                    new_movement.append(move)
                    self.curr_AB_movement.add(move_str)
            inning_movement.append(new_movement)

            self.setupBases(inning_movement)

            # if play (AB) ended and a new play (AB) started, then reset AB trackers to track the next AB
            if (len(all_plays) - 1 > self.curr_play_ind):
                self.plays.append(all_plays[self.curr_play_ind]['result'])
                # if last play was third out, reset outs, bases and current inning plays for the new inning
                # otherwise append the result of last play to current inning plays
                if self.outs != 3:
                    self.curr_inning_plays.append(all_plays[self.curr_play_ind]['result']) 
                else:
                    self.curr_inning_plays.clear()
                    self.outs = 0
                    self.resetBases()
                self.balls = 0
                self.strikes = 0
                self.curr_play_ind = len(all_plays) - 1
                self.curr_AB_ind = 0
                self.curr_AB_events.clear()
                self.curr_AB_movement.clear()
            else: # update ongoing AB (count, current inning plays, current AB events)
                curr_AB = all_plays[self.curr_play_ind]['playEvents']

                # loop through new events in AB, update count and current AB event list
                for i in range(self.curr_AB_ind, len(curr_AB)):
                    print(curr_AB[i])
                    # there can be a "no_pitch" event with code 'N" that has no description, if it is a no_pitch event, do not update anything
                    # if event was a pitch or review decision, then update current balls, strikes, and outs
                    if 'details' in curr_AB[i] and ('call' in curr_AB[i]['details'] and 'code' in curr_AB[i]['details']['call']) or 'reviewDetails' in curr_AB[i]['details']:
                        # if call overturned, re-setup bases and outs
                        #if curr_AB[i]['details']['reviewDetails']['isOverturned']:
                            

                        self.curr_AB_events.append(curr_AB[i]['details']['description'])
                        count_AB = curr_AB[i]['count']
                        self.balls = count_AB['balls']
                        self.strikes = count_AB['strikes']
                        self.outs = count_AB['outs']

                    if self.outs == 3:
                        self.curr_inning_plays.append(all_plays[self.curr_play_ind]['result'])

                self.curr_AB_ind = len(curr_AB)


    

game = Game()
game.setup(717602)
for play in game.plays:
    print(play)
print("runner on first :", game.first)
print("runner on second :", game.second)
print("runner on third :", game.third)
print("balls :", game.balls)
print("strikes :", game.strikes)
print("outs :", game.outs)
print(game.curr_AB_events)
print(game.curr_inning_plays)
'''
while True:
    print("runner on first :", game.first)
    print("runner on second :", game.second)
    print("runner on third :", game.third)
    print("balls :", game.balls)
    print("strikes :", game.strikes)
    print("outs :", game.outs)
    print(game.curr_AB_events)
    print(game.curr_inning_plays)
    
    
    print("updating...\n")
    time.sleep(10)
    game.update()
    print("updated")
'''


    