from Team.team import Team
import random

# 0, 1 self.team_openers
# 2, 3, top order
# 4, 5, 6, middle order
# 7, 8, 9, 10, 11 low order

class StartingEleven:
    def __init__(self):
        self.starting = set()
        self.bench = set()
        self.lineup = []
        self.batting_average = 0
        self.bowling_average = 0
        self.fielding_average = 0
        self.spin_average = 0
        self.pace_average = 0

    def create_starting_eleven(self, team: Team):

        self.team_openers = team.get_team_openers()
        self.team_openers = sorted(self.team_openers, key=lambda Player: Player.batting, reverse=True)
        
        self.team_top_orders = team.get_team_top_order()
        self.team_top_orders = sorted(self.team_top_orders, key=lambda Player: Player.batting, reverse=True)
        
        self.team_mid_orders = team.get_team_mid_order()
        self.team_mid_orders = sorted(self.team_mid_orders, key=lambda Player: Player.batting, reverse=True)
        
        self.team_low_orders = team.get_team_low_order()
        self.team_low_orders = sorted(self.team_low_orders, key=lambda Player: Player.batting, reverse=True)
        
        self.team_pacers = team.get_team_pacers()
        self.team_pacers = sorted(self.team_pacers, key=lambda Player: Player.bowling, reverse=True)
        
        self.team_spinners = team.get_team_spinners()
        self.team_spinners = sorted(self.team_spinners, key=lambda Player: Player.bowling, reverse=True)
        
        self.team_batsmen = team.get_team_batsmen()
        self.team_batsmen = sorted(self.team_batsmen, key=lambda Player: Player.batting, reverse=True)
        self.team_all_rounders = team.get_team_allrounders()
        self.team_all_rounders = sorted(self.team_all_rounders, key=lambda x: (x.batting + x.bowling) / 2, reverse=True)
        
        self.team_wicketkeepers = team.get_team_wicketkeepers()
        self.team_wicketkeepers = sorted(self.team_wicketkeepers, key=lambda Player: Player.batting, reverse=True)

        self.opener_count = 0
        self.top_order_count = 0
        self.mid_order_count = 0
        self.low_order_count = 0
        self.batsmen_count = 0
        self.bowler_count = 0
        self.pacer_count = 0
        self.spinner_count = 0
        self.all_rounder_count = 0
        self.wicketkeeper_count = 0
        print(len(self.starting))
        while(len(self.starting) != 11):
            # create team start
            new_pick = None
            if(self.wicketkeeper_count == 0) and len(self.team_wicketkeepers) > 0:
                new_pick = self.team_wicketkeepers[0]
            elif(self.opener_count + self.top_order_count + self.mid_order_count < 3):
                if(len(self.team_openers) > 0 and len(self.team_top_orders) > 0 and len(self.team_mid_orders) > 0):
                    if (self.team_openers[0].batting > self.team_top_orders[0].batting-10 and self.team_openers[0].batting > self.team_mid_orders[0].batting-20):
                        new_pick = self.team_openers[0]
                    elif (self.team_top_orders[0].batting-10 > self.team_mid_orders[0].batting-20):
                        new_pick = self.team_top_orders[0]
                    else:
                        new_pick = self.team_mid_orders[0]
                elif(len(self.team_openers) == 0 and len(self.team_top_orders) == 0 and len(self.team_mid_orders) == 0):
                    pass
                elif len(self.team_openers) == 0:
                    if(len(self.team_top_orders) != 0):
                        if (self.team_top_orders[0].batting-10 > self.team_mid_orders[0].batting-20):
                            new_pick = self.team_top_orders[0]
                        else:
                            new_pick = self.team_mid_orders[0]
                    else:
                        new_pick = self.team_mid_orders[0]

                elif len(self.team_top_orders) == 0:
                    if(len(self.team_openers) != 0):
                        if (self.team_openers[0].batting > self.team_mid_orders[0].batting-20):
                            new_pick = self.team_openers[0]
                        else:
                            new_pick = self.team_mid_orders[0]
                    else:
                        new_pick = self.team_mid_orders[0]

                elif len(self.team_mid_orders) == 0:
                    if(len(self.team_top_orders) != 0):
                        if (self.team_openers[0].batting > self.team_top_orders[0].batting-10):
                            new_pick = self.team_openers[0]
                        else:
                            new_pick = self.team_top_orders[0]
                    else:
                        new_pick = self.team_top_orders[0]
                else:                                                                                       
                    print("#########################ERROR#########################")
                    break
                    # new_pick = self.team_top_orders[0]
            
            elif(self.bowler_count + self.all_rounder_count < 5 and len(self.team_all_rounders) + len(self.team_pacers) + len(self.team_spinners) != 0):
                pace_pick = None
                spin_pick = None
                rounder_pick = None
                all_rounder_BWL = sorted(self.team_all_rounders, key=lambda x: x.bowling, reverse=True)
                if(len(self.team_pacers) > 0):
                    pace_pick = self.team_pacers[0]
                if(len(self.team_spinners) > 0):
                    spin_pick = self.team_spinners[0]
                if(len(self.team_all_rounders) > 0):
                    rounder_pick = all_rounder_BWL[0]
                if(pace_pick != None and spin_pick != None and rounder_pick != None):
                    if((pace_pick.bowling - self.pacer_count*5) > (spin_pick.bowling - self.spinner_count*5) and (pace_pick.bowling - self.pacer_count*5) > (rounder_pick.bowling - self.spinner_count*5 if rounder_pick.bowling_type == "Spinner" else rounder_pick.bowling - self.pacer_count*5)):
                        new_pick = self.team_pacers[0]

                    elif((spin_pick.bowling - self.spinner_count*5) > (pace_pick.bowling - self.pacer_count*5) and (spin_pick.bowling - self.spinner_count*5) > (rounder_pick.bowling - self.spinner_count*5 if rounder_pick.bowling_type == "Spinner" else rounder_pick.bowling - self.pacer_count*5)):
                        new_pick = self.team_spinners[0]
                
                    elif((rounder_pick.bowling - self.spinner_count*5 if rounder_pick.bowling_type == "Spinner" else rounder_pick.bowling - self.pacer_count*5) >= (pace_pick.bowling - self.pacer_count*5) and (rounder_pick.bowling - self.spinner_count*5 if rounder_pick.bowling_type == "Spinner" else rounder_pick.bowling - self.pacer_count*5) >= (spin_pick.bowling - self.spinner_count*5)):
                        new_pick = all_rounder_BWL[0]
                    elif((spin_pick.bowling - self.spinner_count*5) == (pace_pick.bowling - self.pacer_count*5)):
                        new_pick = random.choice([spin_pick, pace_pick])
                elif(pace_pick == None and spin_pick == None and rounder_pick == None):
                    print("No Bowlers Available")
                    break
                else:
                    if(pace_pick == None):
                        if(spin_pick == None):
                            new_pick = all_rounder_BWL[0]
                        elif(rounder_pick == None):
                            new_pick = self.team_spinners[0]
                        else:
                            if((spin_pick.bowling - self.spinner_count*5) > (rounder_pick.bowling - self.spinner_count*5 if rounder_pick.bowling_type == "Spinner" else rounder_pick.bowling - self.pacer_count*5)):
                                new_pick = self.team_spinners[0]
                            else:
                                new_pick = all_rounder_BWL[0]
                    elif(spin_pick == None):
                        if(pace_pick == None):
                            new_pick = all_rounder_BWL[0]
                        elif(rounder_pick == None):
                            new_pick = self.team_pacers[0]
                        else:
                            if((pace_pick.bowling - self.pacer_count*5) > (rounder_pick.bowling - self.spinner_count*5 if rounder_pick.bowling_type == "Spinner" else rounder_pick.bowling - self.pacer_count*5)):
                                new_pick = self.team_pacers[0]
                            else:
                                new_pick = all_rounder_BWL[0]
                    elif(rounder_pick == None):
                        if(pace_pick == None):
                            new_pick = self.team_spinners[0]
                        elif(spin_pick == None):
                            new_pick = self.team_pacers[0]
                        else:
                            if((spin_pick.bowling - self.spinner_count*5) >= (spin_pick.bowling - self.spinner_count*5)):
                                new_pick = self.team_pacers[0]
                            else:
                                new_pick = self.team_spinners[0]
                    else:
                        print("ONE IS NONE")
                        break
                    # break

            elif(self.batsmen_count + self.all_rounder_count < 5 and len(self.team_batsmen) + len(self.team_all_rounders) > 0 ):
                bat_pick = None
                all_rounder_pick = None
                all_rounder_BAT = sorted(self.team_all_rounders, key=lambda x: x.batting, reverse=True)
                if(len(self.team_batsmen) != 0 and len(self.team_all_rounders) != 0):
                    bat_pick = self.team_batsmen[0]
                    all_rounder_pick = all_rounder_BAT[0]
                    if bat_pick.batting > all_rounder_pick.batting:
                        new_pick = self.team_batsmen[0]
                    else:
                        new_pick = all_rounder_BAT[0]
                elif(len(self.team_batsmen) == 0):
                    new_pick = all_rounder_BAT[0]
                else:
                    new_pick = self.team_batsmen[0]
            
            else:
                print(f'Players Left: {11 - len(self.starting)}')
                merged_bat = self.team_batsmen + self.team_all_rounders
                merged_bowl = self.team_pacers + self.team_spinners + self.team_all_rounders
                print(f"Current Status: Bat-{self.batsmen_count}, All-{self.all_rounder_count} Pace-{self.pacer_count}, Spin-{self.spinner_count}")
                merged_bat = sorted(merged_bat, key=lambda x: x.batting, reverse=True)
                merged_bowl = sorted(merged_bowl, key=lambda x: x.bowling, reverse=True)

                if(len(merged_bat) != 0 and len(merged_bowl) != 0):
                    # if self.batting_average > self.bowling_average:
                    if merged_bat[0].batting - merged_bowl[0].bowling > 5:
                         new_pick = merged_bat[0]
                    elif merged_bowl[0].bowling - merged_bat[0].batting > 5:
                         new_pick = merged_bowl[0]
                    elif self.batsmen_count + self.all_rounder_count < 6:
                    # self.batting_average > self.bowling_average:
                        new_pick = merged_bat[0]
                    elif self.bowler_count + self.all_rounder_count < 6:
                        new_pick = merged_bowl[0]
                    elif self.batting_average > self.bowling_average:
                        new_pick = merged_bowl[0]
                    else:
                        new_pick = merged_bat[0]
                elif(len(merged_bat) != 0):
                    new_pick = merged_bat[0]
                elif(len(merged_bowl) != 0):
                    new_pick = merged_bowl[0]
                else:
                    print("No players left man.")

            if(new_pick == None):
                print("WHY ARE YOU NONE")
                break

            self.starting.add(new_pick)
            self.update_counts(new_pick)
            self.update_average(new_pick)
            # Delete from all lists
            if new_pick in self.team_openers:
                self.team_openers.remove(new_pick)
            if new_pick in self.team_wicketkeepers:
                self.team_wicketkeepers.remove(new_pick)
            if new_pick in self.team_top_orders:
                self.team_top_orders.remove(new_pick)
            if new_pick in self.team_mid_orders:
                self.team_mid_orders.remove(new_pick)
            if new_pick in self.team_low_orders:
                self.team_low_orders.remove(new_pick)
            if new_pick in self.team_pacers:
                self.team_pacers.remove(new_pick)
            if new_pick in self.team_spinners:
                self.team_spinners.remove(new_pick)
            if new_pick in self.team_all_rounders:
                self.team_all_rounders.remove(new_pick)
            if new_pick in self.team_batsmen:
                self.team_batsmen.remove(new_pick)

            # Update Team Average Scores
            print(f'{len(self.starting)}. _picking a {(new_pick.batting_order + " ") if new_pick.position != "Bowler" else ""}{new_pick.position if new_pick.position != "Bowler" else new_pick.bowling_type} -- ', end = "")    
            print(f'{new_pick.name} : BAT({new_pick.batting}) BWL({new_pick.bowling})')
            # self.evaluateTeam()
        
        print("Players _picked: ", len(self.starting))
        print("Openers: ", self.opener_count)
        print("Top Order: ", self.top_order_count)
        print("Mid Order: ", self.mid_order_count)
        print("Low Order: ", self.low_order_count)
        print("Batsmen: ", self.batsmen_count)
        print("Wicketkeeper: ", self.wicketkeeper_count)
        print("Allrounder: ", self.all_rounder_count)
        print("Bowler: ", self.bowler_count)
        print("Pacer: ", self.pacer_count)
        print("Spinner: ", self.spinner_count)
        self.create_lineup()
        self.print_lineup()  

        return self.lineup
        
        # self.batting_average = 0
        # 2 Openers
        # 2 Top or Mid order Batsman
        # 2 Pacers
        # 2 Spinners
        # 1 Wicketkeeper
        # 2 Allrounder
        
    def print_benched_players(self):

        print("")
        print("###PLAYERS LEFT###")
        print("#################")
        print("Openers")
        for x in self.team_openers:
            x.printSummary()
        
        print("#################")
        print("Top-Order")
        for x in self.team_top_orders:
            x.printSummary()

        print("#################")
        print("Middle-Order")
        for x in self.team_mid_orders:
            x.printSummary()

        print("#################")
        print("Low-Order")
        for x in self.team_low_orders:
            x.printSummary()

        print("#################")
        print("Wicketkeepers")
        for x in self.team_wicketkeepers:
            x.printSummary()

        print("#################")
        print("All Rounders")
        for x in self.team_all_rounders:
            x.printSummary()

        print("#################")
        print("Pacers")
        for x in self.team_pacers:
            x.printSummary()

        print("#################")
        print("Spinners")
        for x in self.team_spinners:
            x.printSummary()

    def create_lineup(self):
        eleven = list(self.starting)
        print("Squad Members: ", len(eleven))
        opens = []
        top_ord = []
        mid_ord = []
        low_ord = []

        for x in eleven:
            if(x.batting_order == "Opener"):
                opens.append(x)
            
            elif(x.batting_order == "Top Order"):
                top_ord.append(x)

            elif(x.batting_order == "Middle Order"):
                mid_ord.append(x)
        
            elif(x.batting_order == "Low Order"):
                low_ord.append(x)

        opens = sorted(opens, key=lambda Player: Player.batting, reverse=True)
        top_ord = sorted(top_ord, key=lambda Player: Player.batting, reverse=True)
        mid_ord = sorted(mid_ord, key=lambda Player: Player.batting, reverse=True)
        low_ord = sorted(low_ord, key=lambda Player: Player.batting, reverse=True)

        for x in opens:
            self.lineup.append(x)
        for x in top_ord:
            self.lineup.append(x)
        for x in mid_ord:
            self.lineup.append(x)
        for x in low_ord:
            self.lineup.append(x)
    
    def print_lineup(self):
        for i in range(0, len(self.lineup)):
            print(f'{i+1}. ', end="")
            self.lineup[i].printInLine()
            # print(f'{i+1}. {self.lineup[i].name}: BAT({self.lineup[i].batting}) BWL({self.lineup[i].bowling}) :{self.lineup[i].selling_price}')

    def print_bench(self):
        benchSet = set()
        for x in self.team_openers:
            benchSet.add(x)
        for x in self.team_top_orders:
            benchSet.add(x)
        for x in self.team_mid_orders:
            benchSet.add(x)
        for x in self.team_low_orders:
            benchSet.add(x)
        for x in self.team_wicketkeepers:
            benchSet.add(x)
        for x in self.team_all_rounders:
            benchSet.add(x)
        for x in self.team_pacers:
            benchSet.add(x)
        for x in self.team_spinners:
            benchSet.add(x)

        bench_list = []
        for player in benchSet:
            player.printInLine()
            bench_list.append(player.player_id)

        return bench_list
            # print(f'{player.name}: BAT({player.batting}) BWL({player.bowling})')

        

    def print_team_score(self):
        print(f'Batting Score: {self.batting_average}')
        print(f'Bowling Score: {self.bowling_average}')
        print(f'Spin Score: {self.spin_average}')
        print(f'Pace Score: {self.pace_average}')
        print(f'Fielding Score: {self.fielding_average}')

    def update_counts(self, player):
        if(player.position == "Wicketkeeper"):
            self.wicketkeeper_count = self.wicketkeeper_count + 1
            self.batsmen_count = self.batsmen_count + 1

            
        if(player.position == "Batsmen"):
            self.batsmen_count = self.batsmen_count + 1
            pass
        if(player.position == "Bowler"):
            self.bowler_count = self.bowler_count + 1
            if player.bowling_type == "Spinner":
                self.spinner_count = self.spinner_count + 1
            else:
                self.pacer_count = self.pacer_count + 1
            pass
        if(player.position == "Allrounder"):
            self.all_rounder_count = self.all_rounder_count+1
            if player.bowling_type == "Spinner":
                self.spinner_count = self.spinner_count + 1
            else:
                self.pacer_count = self.pacer_count + 1
            pass
        
        if player.batting_order == "Opener":
            self.opener_count = self.opener_count + 1
        elif player.batting_order == "Top Order":
            self.top_order_count = self.top_order_count + 1
        elif player.batting_order == "Middle Order":
            self.mid_order_count = self.mid_order_count + 1
        else:
            self.low_order_count = self.low_order_count + 1

    def update_average(self, player):
            
            self.fielding_average = ( (self.fielding_average * (len(self.starting) -1)) + player.fielding) / (len(self.starting))

            if player.position == "Batsmen" or player.position == "Wicketkeeper":
                self.batting_average = ( (self.batting_average * (self.batsmen_count + self.all_rounder_count-1)) + player.batting) / (self.batsmen_count + self.all_rounder_count)

            elif player.position == "Bowler":
                self.bowling_average = ( (self.bowling_average * (self.bowler_count + self.all_rounder_count-1)) + player.bowling) / (self.bowler_count + self.all_rounder_count)
                if player.bowling_type == "Pacer":    
                    self.pace_average = ( (self.pace_average * (self.pacer_count-1)) + player.bowling) / self.pacer_count
                else:
                    self.spin_average = ( (self.spin_average * (self.spinner_count-1)) + player.bowling) / self.spinner_count
                pass
            else:
                self.batting_average = ( (self.batting_average * (self.batsmen_count + self.all_rounder_count-1)) + player.batting) / (self.batsmen_count + self.all_rounder_count)
                #UPDATE BOWLING AVERAGE
                self.bowling_average = ( (self.bowling_average * (self.bowler_count + self.all_rounder_count-1)) + player.bowling) / (self.bowler_count + self.all_rounder_count)
                if player.bowling_type == "Pacer":    
                    self.pace_average = ( (self.pace_average * (self.pacer_count-1)) + player.bowling) / self.pacer_count
                else:
                    self.spin_average = ( (self.spin_average * (self.spinner_count-1)) + player.bowling) / self.spinner_count
                pass
    
    
    def evaluate_batting(self):
        batSum = 0
        batter_count = 0
        for player in self.lineup:
            if player.position != "Bowler":
                batSum = batSum + player.batting
                batter_count = batter_count + 1
        batRating = batSum / batter_count
        return round(batRating)
        pass
    def evaluate_bowling(self):
        bowlSum = 0;
        bowler_count = 0
        for player in self.lineup:
            if player.position == "Bowler" or player.position == "Allrounder":
                bowlSum = bowlSum + player.bowling
                bowler_count = bowler_count + 1
        bowlingRating = bowlSum / bowler_count
        return round(bowlingRating)
    
    def evaluate_fielding(self):
        fieldSum = 0
        for player in self.lineup:
            fieldSum = fieldSum + player.fielding
        return round(fieldSum/11)

    def evaluate_lineup(self):
        pass
    def evaluate_team(self):        
        pass