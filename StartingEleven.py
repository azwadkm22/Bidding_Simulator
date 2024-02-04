from TeamGenerator import Team, printTeamPositionAndOrderSummary
import random

# 0, 1 self.teamOpeners
# 2, 3, top order
# 4, 5, 6, middle order
# 7, 8, 9, 10, 11 low order

class StartingEleven:
    def __init__(self):
        self.starting = set()
        self.lineup = []
        self.batting_average = 0
        self.bowling_average = 0
        self.fielding_average = 0
        self.spin_average = 0
        self.pace_average = 0
    def createStartingEleven(self, team):

        self.teamOpeners = team.getTeamOpeners()
        self.teamOpeners = sorted(self.teamOpeners, key=lambda Player: Player.batting, reverse=True)
        
        self.teamTopOrders = team.getTeamTopOrder()
        self.teamTopOrders = sorted(self.teamTopOrders, key=lambda Player: Player.batting, reverse=True)
        
        self.teamMidOrders = team.getTeamMidOrder()
        self.teamMidOrders = sorted(self.teamMidOrders, key=lambda Player: Player.batting, reverse=True)
        
        self.teamLowOrders = team.getTeamLowOrder()
        self.teamLowOrders = sorted(self.teamLowOrders, key=lambda Player: Player.batting, reverse=True)
        
        self.teamPacers = team.getTeamPacers()
        self.teamPacers = sorted(self.teamPacers, key=lambda Player: Player.bowling, reverse=True)
        
        self.teamSpinners = team.getTeamSpinners()
        self.teamSpinners = sorted(self.teamSpinners, key=lambda Player: Player.bowling, reverse=True)
        
        self.teamBatsmen = team.getTeamBatsmen()
        self.teamBatsmen = sorted(self.teamBatsmen, key=lambda Player: Player.batting, reverse=True)
        self.teamAllRounders = team.getTeamAllrounders()
        self.teamAllRounders = sorted(self.teamAllRounders, key=lambda x: (x.batting + x.bowling) / 2, reverse=True)
        
        self.teamWicketkeepers = team.getTeamWicketkeepers()
        self.teamWicketkeepers = sorted(self.teamWicketkeepers, key=lambda Player: Player.batting, reverse=True)

        self.openerCount = 0
        self.topOrderCount = 0
        self.midOrderCount = 0
        self.lowOrderCount = 0
        self.batsmenCount = 0
        self.bowlerCount = 0
        self.pacerCount = 0
        self.spinnerCount = 0
        self.allRounderCount = 0
        self.wickerKeeperCount = 0
        print(len(self.starting))
        while(len(self.starting) != 11):
            # create team start
            newPick = None
            if(self.wickerKeeperCount == 0):
                newPick = self.teamWicketkeepers[0]
            elif(self.openerCount + self.topOrderCount + self.midOrderCount < 3):
                if(len(self.teamOpeners) > 0 and len(self.teamTopOrders) > 0 and len(self.teamMidOrders) > 0):
                    if (self.teamOpeners[0].batting > self.teamTopOrders[0].batting-10 and self.teamOpeners[0].batting > self.teamMidOrders[0].batting-20):
                        newPick = self.teamOpeners[0]
                    elif (self.teamTopOrders[0].batting-10 > self.teamMidOrders[0].batting-20):
                        newPick = self.teamTopOrders[0]
                    else:
                        newPick = self.teamMidOrders[0]
                elif(len(self.teamOpeners) == 0 and len(self.teamTopOrders) == 0 and len(self.teamMidOrders) == 0):
                    pass
                elif len(self.teamOpeners) == 0:
                    if(len(self.teamTopOrders) != 0):
                        if (self.teamTopOrders[0].batting-10 > self.teamMidOrders[0].batting-20):
                            newPick = self.teamTopOrders[0]
                        else:
                            newPick = self.teamMidOrders[0]
                    else:
                        newPick = self.teamMidOrders[0]

                elif len(self.teamTopOrders) == 0:
                    if(len(self.teamOpeners) != 0):
                        if (self.teamOpeners[0].batting > self.teamMidOrders[0].batting-20):
                            newPick = self.teamOpeners[0]
                        else:
                            newPick = self.teamMidOrders[0]
                    else:
                        newPick = self.teamMidOrders[0]

                elif len(self.teamMidOrders) == 0:
                    if(len(self.teamTopOrders) != 0):
                        if (self.teamOpeners[0].batting > self.teamTopOrders[0].batting-10):
                            newPick = self.teamOpeners[0]
                        else:
                            newPick = self.teamTopOrders[0]
                    else:
                        newPick = self.teamTopOrders[0]
                else:                                                                                       
                    print("#########################ERROR#########################")
                    break
                    # newPick = self.teamTopOrders[0]
            
            elif(self.bowlerCount + self.allRounderCount < 5 and len(self.teamAllRounders) + len(self.teamPacers) + len(self.teamSpinners) != 0):
                pacePick = None
                spinPick = None
                rounderPick = None
                all_rounder_BWL = sorted(self.teamAllRounders, key=lambda x: x.bowling, reverse=True)
                if(len(self.teamPacers) > 0):
                    pacePick = self.teamPacers[0]
                if(len(self.teamSpinners) > 0):
                    spinPick = self.teamSpinners[0]
                if(len(self.teamAllRounders) > 0):
                    rounderPick = all_rounder_BWL[0]
                if(pacePick != None and spinPick != None and rounderPick != None):
                    if((pacePick.bowling - self.pacerCount*5) > (spinPick.bowling - self.spinnerCount*5) and (pacePick.bowling - self.pacerCount*5) > (rounderPick.bowling - self.spinnerCount*5 if rounderPick.bowling_type == "Spinner" else rounderPick.bowling - self.pacerCount*5)):
                        newPick = self.teamPacers[0]

                    elif((spinPick.bowling - self.spinnerCount*5) > (pacePick.bowling - self.pacerCount*5) and (spinPick.bowling - self.spinnerCount*5) > (rounderPick.bowling - self.spinnerCount*5 if rounderPick.bowling_type == "Spinner" else rounderPick.bowling - self.pacerCount*5)):
                        newPick = self.teamSpinners[0]
                
                    elif((rounderPick.bowling - self.spinnerCount*5 if rounderPick.bowling_type == "Spinner" else rounderPick.bowling - self.pacerCount*5) >= (pacePick.bowling - self.pacerCount*5) and (rounderPick.bowling - self.spinnerCount*5 if rounderPick.bowling_type == "Spinner" else rounderPick.bowling - self.pacerCount*5) >= (spinPick.bowling - self.spinnerCount*5)):
                        newPick = all_rounder_BWL[0]
                    elif((spinPick.bowling - self.spinnerCount*5) == (pacePick.bowling - self.pacerCount*5)):
                        newPick = random.choice([spinPick, pacePick])
                elif(pacePick == None and spinPick == None and rounderPick == None):
                    print("No Bowlers Available")
                    break
                else:
                    if(pacePick == None):
                        if(spinPick == None):
                            newPick = all_rounder_BWL[0]
                        elif(rounderPick == None):
                            newPick = self.teamSpinners[0]
                        else:
                            if((spinPick.bowling - self.spinnerCount*5) > (rounderPick.bowling - self.spinnerCount*5 if rounderPick.bowling_type == "Spinner" else rounderPick.bowling - self.pacerCount*5)):
                                newPick = self.teamSpinners[0]
                            else:
                                newPick = all_rounder_BWL[0]
                    elif(spinPick == None):
                        if(pacePick == None):
                            newPick = all_rounder_BWL[0]
                        elif(rounderPick == None):
                            newPick = self.teamPacers[0]
                        else:
                            if((pacePick.bowling - self.pacerCount*5) > (rounderPick.bowling - self.spinnerCount*5 if rounderPick.bowling_type == "Spinner" else rounderPick.bowling - self.pacerCount*5)):
                                newPick = self.teamPacers[0]
                            else:
                                newPick = all_rounder_BWL[0]
                    elif(rounderPick == None):
                        if(pacePick == None):
                            newPick = self.teamSpinners[0]
                        elif(spinPick == None):
                            newPick = self.teamPacers[0]
                        else:
                            if((spinPick.bowling - self.spinnerCount*5) >= (spinPick.bowling - self.spinnerCount*5)):
                                newPick = self.teamPacers[0]
                            else:
                                newPick = self.teamSpinners[0]
                    else:
                        print("ONE IS NONE")
                        break
                    # break

            elif(self.batsmenCount + self.allRounderCount < 5 and len(self.teamBatsmen) + len(self.teamAllRounders) > 0 ):
                batPick = None
                allRounderPick = None
                all_rounder_BAT = sorted(self.teamAllRounders, key=lambda x: x.batting, reverse=True)
                if(len(self.teamBatsmen) != 0 and len(self.teamAllRounders) != 0):
                    batPick = self.teamBatsmen[0]
                    allRounderPick = all_rounder_BAT[0]
                    if batPick.batting > allRounderPick.batting:
                        newPick = self.teamBatsmen[0]
                    else:
                        newPick = all_rounder_BAT[0]
                elif(len(self.teamBatsmen) == 0):
                    newPick = all_rounder_BAT[0]
                else:
                    newPick = self.teamBatsmen[0]
            
            else:
                print(f'Players Left: {11 - len(self.starting)}')
                mergedBat = self.teamBatsmen + self.teamAllRounders
                mergedBowl = self.teamPacers + self.teamSpinners + self.teamAllRounders

                mergedBat = sorted(mergedBat, key=lambda x: x.batting, reverse=True)
                mergedBowl = sorted(mergedBowl, key=lambda x: x.bowling, reverse=True)

                if(len(mergedBat) != 0 and len(mergedBowl) != 0):
                    if self.batting_average > self.bowling_average:
                        newPick = mergedBowl[0]
                    else:
                        newPick = mergedBat[0]
                elif(len(mergedBat) != 0):
                    newPick = mergedBat[0]
                elif(len(mergedBowl) != 0):
                    newPick = mergedBowl[0]
                else:
                    print("No players left man.")

            if(newPick == None):
                print("WHY ARE YOU NONE")
                break

            self.starting.add(newPick)
            self.updateCounts(newPick)
            self.updateAverage(newPick)
            # Delete from all lists
            if newPick in self.teamOpeners:
                self.teamOpeners.remove(newPick)
            if newPick in self.teamWicketkeepers:
                self.teamWicketkeepers.remove(newPick)
            if newPick in self.teamTopOrders:
                self.teamTopOrders.remove(newPick)
            if newPick in self.teamMidOrders:
                self.teamMidOrders.remove(newPick)
            if newPick in self.teamLowOrders:
                self.teamLowOrders.remove(newPick)
            if newPick in self.teamPacers:
                self.teamPacers.remove(newPick)
            if newPick in self.teamSpinners:
                self.teamSpinners.remove(newPick)
            if newPick in self.teamAllRounders:
                self.teamAllRounders.remove(newPick)
            if newPick in self.teamBatsmen:
                self.teamBatsmen.remove(newPick)

            # Update Team Average Scores
            print(f'Picking a {(newPick.batting_order + " ") if newPick.position != "Bowler" else ""}{newPick.position if newPick.position != "Bowler" else newPick.bowling_type}')    
            print(f'{len(self.starting)}. {newPick.name} : BAT({newPick.batting}) BWL({newPick.bowling})')
            # self.evaluateTeam()
        
        print("Players Picked: ", len(self.starting))
        print("Openers: ", self.openerCount)
        print("Top Order: ", self.topOrderCount)
        print("Mid Order: ", self.midOrderCount)
        print("Low Order: ", self.lowOrderCount)
        print("Batsmen: ", self.batsmenCount)
        print("Wicketkeeper: ", self.wickerKeeperCount)
        print("Allrounder: ", self.allRounderCount)
        print("Bowler: ", self.bowlerCount)
        print("Pacer: ", self.pacerCount)
        print("Spinner: ", self.spinnerCount)
        self.createLineup()
        self.printLineup()  
        
        # self.batting_average = 0
        # 2 Openers
        # 2 Top or Mid order Batsman
        # 2 Pacers
        # 2 Spinners
        # 1 Wicketkeeper
        # 2 Allrounder
        
    def printBenchedPlayers(self):

        print("")
        print("###PLAYERS LEFT###")
        print("#################")
        print("Openers")
        for x in self.teamOpeners:
            x.printSummary()
        
        print("#################")
        print("Top-Order")
        for x in self.teamTopOrders:
            x.printSummary()

        print("#################")
        print("Middle-Order")
        for x in self.teamMidOrders:
            x.printSummary()

        print("#################")
        print("Low-Order")
        for x in self.teamLowOrders:
            x.printSummary()

        print("#################")
        print("Wicketkeepers")
        for x in self.teamWicketkeepers:
            x.printSummary()

        print("#################")
        print("All Rounders")
        for x in self.teamAllRounders:
            x.printSummary()

        print("#################")
        print("Pacers")
        for x in self.teamPacers:
            x.printSummary()

        print("#################")
        print("Spinners")
        for x in self.teamSpinners:
            x.printSummary()

    def createLineup(self):
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
    
    def printLineup(self):
        for i in range(0, len(self.lineup)):
            print(f'{i+1}. {self.lineup[i].name}: BAT({self.lineup[i].batting}) BWL({self.lineup[i].bowling})')
    def printTeamScore(self):
        print(f'Batting Score: {self.batting_average}')
        print(f'Bowling Score: {self.bowling_average}')
        print(f'Spin Score: {self.spin_average}')
        print(f'Pace Score: {self.pace_average}')
        print(f'Fielding Score: {self.fielding_average}')
    def updateCounts(self, player):
        if(player.position == "Wicketkeeper"):
            self.wickerKeeperCount = self.wickerKeeperCount + 1
            self.batsmenCount = self.batsmenCount + 1

            
        if(player.position == "Batsmen"):
            self.batsmenCount = self.batsmenCount + 1
            pass
        if(player.position == "Bowler"):
            self.bowlerCount = self.bowlerCount + 1
            if player.bowling_type == "Spinner":
                self.spinnerCount = self.spinnerCount + 1
            else:
                self.pacerCount = self.pacerCount + 1
            pass
        if(player.position == "Allrounder"):
            self.allRounderCount = self.allRounderCount+1
            if player.bowling_type == "Spinner":
                self.spinnerCount = self.spinnerCount + 1
            else:
                self.pacerCount = self.pacerCount + 1
            pass
        
        if player.batting_order == "Opener":
            self.openerCount = self.openerCount + 1
        elif player.batting_order == "Top Order":
            self.topOrderCount = self.topOrderCount + 1
        elif player.batting_order == "Middle Order":
            self.midOrderCount = self.midOrderCount + 1
        else:
            self.lowOrderCount = self.lowOrderCount + 1

    def updateAverage(self, player):
            
            self.fielding_average = ( (self.fielding_average * (len(self.starting) -1)) + player.fielding) / (len(self.starting))

            if player.position == "Batsmen" or player.position == "Wicketkeeper":
                self.batting_average = ( (self.batting_average * (self.batsmenCount + self.allRounderCount-1)) + player.batting) / (self.batsmenCount + self.allRounderCount)

            elif player.position == "Bowler":
                self.bowling_average = ( (self.bowling_average * (self.bowlerCount + self.allRounderCount-1)) + player.bowling) / (self.bowlerCount + self.allRounderCount)
                if player.bowling_type == "Pacer":    
                    self.pace_average = ( (self.pace_average * (self.pacerCount-1)) + player.bowling) / self.pacerCount
                else:
                    self.spin_average = ( (self.spin_average * (self.spinnerCount-1)) + player.bowling) / self.spinnerCount
                pass
            else:
                self.batting_average = ( (self.batting_average * (self.batsmenCount + self.allRounderCount-1)) + player.batting) / (self.batsmenCount + self.allRounderCount)
                #UPDATE BOWLING AVERAGE
                self.bowling_average = ( (self.bowling_average * (self.bowlerCount + self.allRounderCount-1)) + player.bowling) / (self.bowlerCount + self.allRounderCount)
                if player.bowling_type == "Pacer":    
                    self.pace_average = ( (self.pace_average * (self.pacerCount-1)) + player.bowling) / self.pacerCount
                else:
                    self.spin_average = ( (self.spin_average * (self.spinnerCount-1)) + player.bowling) / self.spinnerCount
                pass
    def evaluateBatting(self):
        
        pass
    def evaluateBowling(self):
        pass
    def evaluateFielding(self):
        pass

    def evaluateLineup(self):
        pass
    def evaluateTeam(self):

    
        # batting_average
        # bowling_average
        # fielding_average

        # opening_rating
        # top_order_rating
        # mid_order_rating
        # low_order_rating
        
        # pace_average
        # spin_average
        
        # wicketkeeper

        
        pass