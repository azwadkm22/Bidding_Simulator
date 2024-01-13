import random
from PlayerGenerator import Player

class Team:
    
    def __init__(self, TeamName):
        self.name = TeamName
        self.playerList = []
        self.number_of_players = 0
        self.number_of_batsmen = 0
        self.number_of_bowlers = 0
        self.number_of_allrounders = 0
        self.number_of_wicketkeepers = 0
        self.number_of_pacers = 0
        self.number_of_spinners = 0
        self.number_of_stars = 0
        self.batting_average = 0
        self.bowling_average = 0
        self.fielding_average = 0
        self.pace_bowling_average = 0
        self.spin_bowling_average = 0
        self.number_of_openers = 0
        self.number_of_right_handed_batsmen = 0
        self.number_of_left_handed_batsmen = 0
        self.top_order_batsmen = 0
        self.mid_order_batsmen = 0
        self.low_order_batsmen = 0
        self.teamRating = 0
        self.fame_average = 0
    
    def addPlayer(self, player):
        self.playerList.append(player)
        self.number_of_players = self.number_of_players + 1
        self.fielding_average = ( (self.fielding_average * (self.number_of_players-1)) + player.fielding) / self.number_of_players
        #Handle Stars
        if(player.fame > 80):
            self.number_of_stars = self.number_of_stars + 1

        self.fame_average = ( (self.fame_average * (self.number_of_players-1)) + player.fame) / self.number_of_players
        #Handle Bowling
        if(player.position == "Bowler"):
            self.number_of_bowlers = self.number_of_bowlers + 1
            self.bowling_average = ( (self.bowling_average * (self.number_of_bowlers-1)) + player.bowling) / self.number_of_bowlers
            if player.bowling_type == "Pacer":    
                self.number_of_pacers = self.number_of_pacers +1
                self.pace_bowling_average = ( (self.pace_bowling_average * (self.number_of_pacers-1)) + player.bowling) / self.number_of_pacers
            else:
                self.number_of_spinners = self.number_of_spinners +1
                self.spin_bowling_average = ( (self.spin_bowling_average * (self.spin_bowling_average-1)) + player.bowling) / self.number_of_spinners
        
        else: # IF NOT BOWLER THEN MUST BE BATSMEN
            self.number_of_batsmen = self.number_of_batsmen +1
            if player.batting_hand == "Right":
                self.number_of_right_handed_batsmen = self.number_of_right_handed_batsmen + 1
            else:
                self.number_of_left_handed_batsmen = self.number_of_left_handed_batsmen + 1

            if player.batting_order == "Top Order":
                self.top_order_batsmen = self.top_order_batsmen + 1
            elif player.batting_order == "Middle Order":
                self.mid_order_batsmen = self.mid_order_batsmen + 1
            elif player.batting_order == "Low Order":
                self.low_order_batsmen = self.low_order_batsmen + 1
            else:
                self.number_of_openers = self.number_of_openers + 1
            

            #UPDATE BATTING AVERAGE
            self.batting_average = ( (self.batting_average * (self.number_of_batsmen-1)) + player.batting) / self.number_of_batsmen


            if(player.position == "Allrounder"):
                self.number_of_allrounders = self.number_of_allrounders + 1
                #UPDATE BOWLING AVERAGE
                self.number_of_bowlers = self.number_of_bowlers + 1
                self.bowling_average = ( (self.bowling_average * (self.number_of_bowlers-1)) + player.bowling) / self.number_of_bowlers
                if player.bowling_type == "Pacer":    
                    self.number_of_pacers = self.number_of_pacers +1
                    self.pace_bowling_average = ( (self.pace_bowling_average * (self.number_of_pacers-1)) + player.bowling) / self.number_of_pacers
                else:
                    self.number_of_spinners = self.number_of_spinners +1
                    self.spin_bowling_average = ( (self.spin_bowling_average * (self.number_of_spinners-1)) + player.bowling) / self.number_of_spinners

            if(player.position == "Wicketkeeper"):
                self.number_of_wicketkeepers = self.number_of_wicketkeepers + 1

    
    def printTeamData(self):
        print(self.name)
        print("============================")
        print("Player Count: ", self.number_of_players)
        print("Batsmen Count: ", self.number_of_batsmen)
        print("Bowler Count: ", self.number_of_bowlers)
        print("Wicketkeeper Count: ", self.number_of_wicketkeepers)
        print("Allrounder Count: ", self.number_of_allrounders)
        print("###   BATTING   ###")
        print("Batsmen Count: ", self.number_of_batsmen)
        print("Batting Average: ", self.batting_average)
        print("Opener Count: ", self.number_of_openers)
        print("Top Order Count: ", self.top_order_batsmen)
        print("Mid Order Count: ", self.mid_order_batsmen)
        print("Low Order Count: ", self.low_order_batsmen)
        print("Right Handed : Left Handed: ", self.number_of_right_handed_batsmen, " : ", self.number_of_left_handed_batsmen)
        print("###  BOWLING   ###")
        print("Bowler Count: ", self.number_of_bowlers)
        print("Bowling Average: ", self.bowling_average)
        print("Number of Pacers: ", self.number_of_pacers)
        print("Pace Bowling Average: ", self.pace_bowling_average)
        print("Number of Spinners: ", self.number_of_spinners)
        print("Spin Bowling Average: ", self.spin_bowling_average)
        print("### FAME ###", self.fame_average)
        print("Fielding Average", self.fielding_average)

    def printTeamPlayerData(self):
        print(self.name)
        print("============================")
        print("Player Count: ", self.number_of_players)
        print("Batsmen Count: ", self.number_of_batsmen - self.number_of_allrounders)
        print("Bowler Count: ", self.number_of_bowlers - self.number_of_allrounders)
        print("Wicketkeeper Count: ", self.number_of_wicketkeepers)
        print("Allrounder Count: ", self.number_of_allrounders)

    def findNewPlayerPriority(self, player):
        priority = 0
        if player.position == "Bowler" or (player.position == "Allrounder" and player.bowling > 60):
            if player.bowling_type == "Spinner":
                if self.number_of_spinners < 3:
                    priority = priority + 1
                if self.spin_bowling_average < player.bowling:
                    priority = priority + 1
            if player.bowling_type == "Pacer":
                if self.number_of_pacers < 3:
                    priority = priority + 1
                if self.pace_bowling_average < player.bowling:
                    priority = priority + 1
            if player.bowling > 70 and self.number_of_bowlers < 4:
                priority = priority + 1
            if player.bowling > self.bowling_average:
                priority = priority + 1

            if player.bowling < 50:
                priority = 1    
            

        if player.position == "Batsmen" or (player.position == "Allrounder" and player.batting > 60) or player.position == "Wicketkeeper":
            if player.batting_hand == "Right":
                if self.number_of_right_handed_batsmen < 3:
                    priority = priority + 1
            
            if player.batting_hand == "left":
                if self.number_of_left_handed_batsmen < 3:
                    priority = priority + 1
                
            if player.batting > 70 and self.number_of_batsmen < 6:
                priority = priority + 1
            
            if self.batting_average < player.batting:
                priority = priority + 1

            if player.batting_order == "Opener" and self.number_of_openers == 0:
                priority = priority + 3
            if player.batting_order == "Opener" and self.number_of_openers < 3:
                priority = priority + 1
            if player.batting_order == "Middle Order" and self.mid_order_batsmen < 3:
                priority = priority + 1
            if player.batting_order == "Top Order" and self.mid_order_batsmen < 2:
                priority = priority + 1
            if player.batting_order == "Low Order" and self.low_order_batsmen < 1:
                priority = priority + 1
            if player.position == "Wicketkeeper" and self.number_of_wicketkeepers < 1:
                priority = priority + 5
            if player.position == "Wicketkeeper" and self.number_of_wicketkeepers < 2:
                priority = priority + 1

            if player.batting < 50:
                priority = 1
        return priority
    
    def printAllPlayerData(self):
        for p in self.playerList:
            p.printDetails()
            print()
        



    def findMostPopular(self):
        fame = -1
        famous_player = 0
        for p in self.playerList:
            if p.fame > fame:
                fame = p.fame
                famous_player = p
        return famous_player
    
    def findBestBatsman(self):
        bat = -1
        best_batsman = 0
        for p in self.playerList:
            if p.batting > bat:
                bat = p.batting
                best_batsman = p
        return best_batsman
    
    def findBestBowler(self):
        bat = -1
        best_bowler = 0
        for p in self.playerList:
            if p.bowling > bat:
                bat = p.bowling
                best_bowler = p
        
        return best_bowler




# Team1 = Team("Dhaka Gladiators")

# for i in range(23):
#     a = Player()
#     Team1.addPlayer(a)
#     # x = input()
#     # if x == " ":

# # Team1.printTeamPlayerData()
# Team1.printTeamData()

# print("")
# print("")


# print("MOST FAMOUS")

# print("")
# famP = Team1.findMostPopular()
# famP.printDetails()


# print("BEST BATTING")

# print("")
# famP = Team1.findBestBowler()
# famP.printDetails()


# print("BEST BOWLING")

# print("")
# famP = Team1.findBestBatsman()
# famP.printDetails()
