import random
from Player.player import Player

def print_team_position_and_order_details(team):

        openers = team.get_team_Openers()
        openers = sorted(openers, key=lambda Player: Player.batting, reverse=True)
        
        top_orders = team.get_team_TopOrder()
        top_orders = sorted(top_orders, key=lambda Player: Player.batting, reverse=True)
        
        mid_orders = team.get_team_MidOrder()
        mid_orders = sorted(mid_orders, key=lambda Player: Player.batting, reverse=True)
        
        low_order = team.get_team_LowOrder()
        low_order = sorted(low_order, key=lambda Player: Player.batting, reverse=True)
        
        pacers = team.get_team_Pacers()
        pacers = sorted(pacers, key=lambda Player: Player.bowling, reverse=True)
        
        spinners = team.get_team_Spinners()
        spinners = sorted(spinners, key=lambda Player: Player.bowling, reverse=True)
        
        all_rounders = team.get_team_Allrounders()
        all_rounders = sorted(all_rounders, key=lambda x: (x.batting + x.bowling) / 2, reverse=True)
        
        wicketkeepers = team.get_team_Wicketkeepers()
        wicketkeepers = sorted(wicketkeepers, key=lambda Player: Player.batting, reverse=True)

        print("")
    
        print("")
        print("Openers", len(openers))
        for p in openers:
            p.printDetails()
            print("")
        print()
        print("Top Order", len(top_orders))
        for p in top_orders:
            p.printDetails()
            print("")
        print()
        print("Middle Order", len(mid_orders))
        for p in mid_orders:
            p.printDetails()

            print("")
        print()
        print("Low Order", len(low_order))
        for p in low_order:
            p.printDetails()
        
            print("")
        print()
        print("Wicketkeepers", len(wicketkeepers))
        for p in wicketkeepers:
            p.printDetails()
            print("")
        print()
        print("All Rounders", len(all_rounders))
        for p in all_rounders:
            p.printDetails()
            print("")
        print()
        print("Spinners", len(spinners))
        for p in spinners:
            p.printDetails()
            print("")
        print()
        print("Pacers", len(pacers))
        for p in pacers:
            p.printDetails()
            print("")

def print_team_position_and_order_summary(team):
        openers = team.get_team_Openers()
        openers = sorted(openers, key=lambda Player: Player.batting, reverse=True)
        
        top_orders = team.get_team_TopOrder()
        top_orders = sorted(top_orders, key=lambda Player: Player.batting, reverse=True)
        
        mid_orders = team.get_team_MidOrder()
        mid_orders = sorted(mid_orders, key=lambda Player: Player.batting, reverse=True)
        
        low_order = team.get_team_LowOrder()
        low_order = sorted(low_order, key=lambda Player: Player.batting, reverse=True)
        
        pacers = team.get_team_Pacers()
        pacers = sorted(pacers, key=lambda Player: Player.bowling, reverse=True)
        
        spinners = team.get_team_Spinners()
        spinners = sorted(spinners, key=lambda Player: Player.bowling, reverse=True)
        
        all_rounders = team.get_team_Allrounders()
        all_rounders = sorted(all_rounders, key=lambda x: (x.batting + x.bowling) / 2, reverse=True)
        
        wicketkeepers = team.get_team_Wicketkeepers()
        wicketkeepers = sorted(wicketkeepers, key=lambda Player: Player.batting, reverse=True)

        print("")
        print("")
        print("Openers", len(openers))
        for p in openers:
            p.printSummary()
            print("")
        print()
        print("Top Order", len(top_orders))
        for p in top_orders:
            p.printSummary()
            print("")
        print()
        print("Middle Order", len(mid_orders))
        for p in mid_orders:
            p.printSummary()

            print("")
        print()
        print("Low Order", len(low_order))
        for p in low_order:
            p.printSummary()
        
            print("")
        print()
        print("Wicketkeepers", len(wicketkeepers))
        for p in wicketkeepers:
            p.printSummary()
            print("")
        print()
        print("All Rounders", len(all_rounders))
        for p in all_rounders:
            p.printSummary()
            print("")
        print()
        print("Spinners", len(spinners))
        for p in spinners:
            p.printSummary()
            print("")
        print()
        print("Pacers", len(pacers))
        for p in pacers:
            p.printSummary()
            print("")


class Team:
    def __init__(self, team_name):
        self.name = team_name
        self.player_list = []
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
    
    def addPlayer(self, player: Player):
        self.player_list.append(player)
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
                self.spin_bowling_average = ( (self.spin_bowling_average * (self.number_of_spinners-1)) + player.bowling) / self.number_of_spinners
        
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

    def print_team_ata(self):
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

    def print_team_player_data(self):
        print(self.name)
        print("============================")
        print("Player Count: ", self.number_of_players)
        print("Batsmen Count: ", self.number_of_batsmen - self.number_of_allrounders)
        print("Bowler Count: ", self.number_of_bowlers - self.number_of_allrounders)
        print("Wicketkeeper Count: ", self.number_of_wicketkeepers)
        print("Allrounder Count: ", self.number_of_allrounders)

    def find_new_player_priority(self, player):
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
    
    def print_all_player_data(self):
        for p in self.player_list:
            p.printDetails()
            print()
        
    def get_team_openers(self):
        openerList = []
        for p in self.player_list:
            if p.batting_order == "Opener":
                openerList.append(p)
        return openerList

    def get_team_top_order(self):
        topOrderList = []
        for p in self.player_list:
            if p.batting_order == "Top Order":
                topOrderList.append(p)
        return topOrderList

    def get_team_mid_order(self):
        midOrderList = []
        for p in self.player_list:
            if p.batting_order == "Middle Order":
                midOrderList.append(p)
        return midOrderList
    
    def get_team_low_order(self):
        lowOrderList = []
        for p in self.player_list:
            if p.batting_order == "Low Order":
                lowOrderList.append(p)
        return lowOrderList

    def get_team_pacers(self):
        pacerList = []
        for p in self.player_list:
            if p.position == "Bowler" or p.position == "Allrounder":
                if p.bowling_type == "Pacer":
                    pacerList.append(p)
        return pacerList

    def get_team_spinners(self):
        spinnerList = []
        for p in self.player_list:
            if p.position == "Bowler" or p.position == "Allrounder":
                if p.bowling_type == "Spinner":
                    spinnerList.append(p)
        return spinnerList

    def get_team_batsmen(self):
        batsmenList = []
        for p in self.player_list:
            if p.position == "Batsmen" or p.position == "Wicketkeeper":
                batsmenList.append(p)
        return batsmenList
    
    def get_team_allrounders(self):
        all_rounderList = []
        for p in self.player_list:
            if p.position == "Allrounder":
                all_rounderList.append(p)
        return all_rounderList

    def get_team_wicketkeepers(self):
        wkList = []
        for p in self.player_list:
            if p.position == "Wicketkeeper":
                wkList.append(p)
        return wkList


    def find_most_popular(self):
        fame = -1
        famous_player = 0
        for p in self.player_list:
            if p.fame > fame:
                fame = p.fame
                famous_player = p
        return famous_player
    
    def find_best_batsman(self):
        bat = -1
        best_batsman = 0
        for p in self.player_list:
            if p.batting > bat:
                bat = p.batting
                best_batsman = p
        return best_batsman
    
    def find_best_bowler(self):
        bat = -1
        best_bowler = 0
        for p in self.player_list:
            if p.bowling > bat:
                bat = p.bowling
                best_bowler = p
        
        return best_bowler
    
    def find_bowlers_of_type(self, bowling_type):
        if bowling_type == "Spinner":
            spin = self.get_team_spinners()
            all_r = self.get_team_allrounders()
            ret = []
            for p in spin:
                if p not in all_r:
                    ret.append(p)
            return ret
        
        if bowling_type == "Pacer":
            pace = self.get_team_pacers()
            all_r = self.get_team_allrounders()
            ret = []
            for p in pace:
                if p not in all_r:
                    ret.append(p)
            return ret
        
    def findSimilarTeamPlayers(self, player):
        if player.position == 'Bowler':
            return self.find_bowlers_of_type(player.bowling_type)
        
        elif player.position == "Allrounder":
            return self.get_team_allrounders()
        
        elif player.position == "Batsmen":
            return self.get_team_batsmen()
        
        elif player.position == "Wicketkeeper":
            return self.get_team_wicketkeepers()

    def get_team_data_to_JSON(self):
        team_data = {}
        
        team_data["team_name"] = self.name
        team_data["number_of_players"] = self.number_of_players
        team_data["number_of_batsmen"] = self.number_of_batsmen
        team_data["number_of_bowlers"] = self.number_of_bowlers
        team_data["number_of_allrounders"] = self.number_of_allrounders
        team_data["number_of_wicketkeepers"] = self.number_of_wicketkeepers
        team_data["number_of_pacers"] = self.number_of_pacers
        team_data["number_of_spinners"] = self.number_of_spinners
        team_data["number_of_stars"] = self.number_of_stars
        team_data["batting_average"] = self.batting_average
        team_data["bowling_average"] = self.bowling_average
        team_data["fielding_average"] = self.fielding_average
        team_data["pace_bowling_average"] = self.pace_bowling_average
        team_data["spin_bowling_average"] = self.spin_bowling_average
        team_data["number_of_openers"] = self.number_of_openers
        team_data["number_of_right_handed_batsmen"] = self.number_of_right_handed_batsmen
        team_data["number_of_left_handed_batsmen"] = self.number_of_left_handed_batsmen
        team_data["top_order_batsmen"] = self.top_order_batsmen
        team_data["mid_order_batsmen"] = self.mid_order_batsmen
        team_data["low_order_batsmen"] = self.low_order_batsmen
        team_data["teamRating"] = self.teamRating
        team_data["fame_average"] = self.fame_average
        team_data["players_data"] = {}
        for p in self.player_list:
            team_data["players_data"][p.player_id] = p.get_JSON_data()
        
        return team_data



# Team1 = Team("Dhaka Gladiators")

# for i in range(23):
#     a = Player()
#     Team1.addPlayer(a)
#     # x = input()
#     # if x == " ":

# # Team1.print_team_player_data()
# Team1.print_team_ata()

# print("")
# print("")


# print("MOST FAMOUS")

# print("")
# famP = Team1.find_mostPopular()
# famP.printDetails()


# print("BEST BATTING")

# print("")
# famP = Team1.find_best_Bowler()
# famP.printDetails()


# print("BEST BOWLING")

# print("")
# famP = Team1.find_best_Batsman()
# famP.printDetails()
