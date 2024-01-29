from TeamGenerator import Team, printTeamPositionAndOrderSummary


# 0, 1 openers
# 2, 3, top order
# 4, 5, 6, middle order
# 7, 8, 9, 10, 11 low order

class StartingEleven:
    def __init__(self):
        self.starting = set()
        self.lineup = []
    def createStartingEleven(self, team):

        openers = team.getTeamOpeners()
        openers = sorted(openers, key=lambda Player: Player.batting, reverse=True)
        
        top_orders = team.getTeamTopOrder()
        top_orders = sorted(top_orders, key=lambda Player: Player.batting, reverse=True)
        
        mid_orders = team.getTeamMidOrder()
        mid_orders = sorted(mid_orders, key=lambda Player: Player.batting, reverse=True)
        
        low_order = team.getTeamLowOrder()
        low_order = sorted(low_order, key=lambda Player: Player.batting, reverse=True)
        
        pacers = team.getTeamPacers()
        pacers = sorted(pacers, key=lambda Player: Player.bowling, reverse=True)
        
        spinners = team.getTeamSpinners()
        spinners = sorted(spinners, key=lambda Player: Player.bowling, reverse=True)
        
        batsmen = team.getTeamBatsmen()
        batsmen = sorted(batsmen, key=lambda Player: Player.batting, reverse=True)
        all_rounders = team.getTeamAllrounders()
        all_rounders = sorted(all_rounders, key=lambda x: (x.batting + x.bowling) / 2, reverse=True)
        
        wicketkeepers = team.getTeamWicketkeepers()
        wicketkeepers = sorted(wicketkeepers, key=lambda Player: Player.batting, reverse=True)

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
        # starting.add(wicketkeepers[0])
        # starting.add(openers[0])
        # starting.add(openers[1])
        # # starting.add(pacers[0])
        # # starting.add(spinners[0])
        # # starting.add(spinners[0])

        # # if len(openers > )
        # starting.add(openers[1])
        while(len(self.starting) != 11):
            # create team start
            newPick = None
            if(self.wickerKeeperCount == 0):
                newPick = wicketkeepers[0]
            elif(self.openerCount + self.topOrderCount < 3):
                if(len(openers) > 0):
                    if (openers[0].batting > top_orders[0].batting-10):
                        newPick = openers[0]
                    else:
                        newPick = top_orders[0]
                else:
                    newPick = top_orders[0]
            
            elif(self.bowlerCount + self.allRounderCount < 6):
                pacePick = None
                spinPick = None
                rounderPick = None
                if(len(pacers) > 0):
                    pacePick = pacers[0]
                if(len(spinners) > 0):
                    spinPick = spinners[0]
                if(len(all_rounders) > 0):
                    rounderPick = all_rounders[0]
                if(pacePick != None and spinPick != None and rounderPick != None):
                    if(pacePick.bowling >= spinPick.bowling and pacePick.bowling >= rounderPick.bowling):
                        newPick = pacers[0]

                    elif(spinPick.bowling >= pacePick.bowling and spinPick.bowling >= rounderPick.bowling):
                        newPick = spinners[0]
               
                    elif(rounderPick.bowling >= pacePick.bowling and rounderPick.bowling >= spinPick.bowling):
                        newPick = all_rounders[0]
                else:
                    if(pacePick == None):
                        if(spinPick.bowling >= rounderPick.bowling):
                            newPick = spinners[0]
                        else:
                            newPick = all_rounders[0]
                    elif(spinPick == None):
                        if(pacePick.bowling >= rounderPick.bowling):
                            newPick = pacers[0]
                        else:
                            newPick = all_rounders[0]
                    else:
                        if(pacePick.bowling >= spinPick.bowling):
                            newPick = spinners[0]
                    print("ONE IS NONE")
                    break
            
            elif(self.batsmenCount + self.allRounderCount < 6):
                batPick = batsmen[0]
                allRounderPick = all_rounders[0]
                if(batPick != None and allRounderPick != None):
                    if batPick.batting > allRounderPick.batting:
                        newPick = batPick
                    else:
                        newPick = allRounderPick
                elif(batPick == None):
                    newPick = allRounderPick
                else:
                    newPick = batPick
            
            else:
                pass
                # break
            if(newPick == None):
                print("WHY ARE YOU NONE")
                break

            self.starting.add(newPick)
            self.updateCounts(newPick)
            # Delete from all lists
            if newPick in openers:
                openers.remove(newPick)
            if newPick in wicketkeepers:
                wicketkeepers.remove(newPick)
            if newPick in top_orders:
                top_orders.remove(newPick)
            if newPick in mid_orders:
                mid_orders.remove(newPick)
            if newPick in low_order:
                low_order.remove(newPick)
            if newPick in pacers:
                pacers.remove(newPick)
            if newPick in spinners:
                spinners.remove(newPick)
            if newPick in all_rounders:
                all_rounders.remove(newPick)
            if newPick in batsmen:
                batsmen.remove(newPick)
        
        
        print("Players Picked: ", len(self.starting))
        print("Openers: ", self.openerCount)
        print("Top Order: ", self.topOrderCount)
        print("Mid Order: ", self.midOrderCount)
        print("Low Order: ", self.lowOrderCount)
        print("Batsmen: ", self.batsmenCount)
        print("Wickerkeeper: ", self.wickerKeeperCount)
        print("Allrounder: ", self.allRounderCount)
        print("Bowler: ", self.bowlerCount)
        print("Pacer: ", self.pacerCount)
        print("Spinner: ", self.spinnerCount)
        print("Players Picked: ", len(self.starting))
        for x in self.starting:
            x.printName()

        self.createLineup()
        self.printLineup()  
        # print("")
        # print("###PLAYERS LEFT###")
        # print("#################")
        # print("Openers")
        # for x in openers:
        #     x.printSummary()
        # print("Wicketkeepers")
        # for x in wicketkeepers:
        #     x.printSummary()
        
        # print("#################")
        # print("Top-Order")
        # for x in top_orders:
        #     x.printSummary()

        # print("#################")
        # print("Middle-Order")
        # for x in mid_orders:
        #     x.printSummary()

        # print("#################")
        # print("Low-Order")
        # for x in low_order:
        #     x.printSummary()

        # print("#################")
        # print("All Rounders")
        # for x in all_rounders:
        #     x.printSummary()

        # print("#################")
        # print("Pacers")
        # for x in pacers:
        #     x.printSummary()

        # print("#################")
        # print("Spinners")
        # for x in spinners:
        #     x.printSummary()

        # self.batting_overall = 0
        # 2 Openers
        # 2 Top or Mid order Batsman
        # 2 Pacers
        # 2 Spinners
        # 1 Wicketkeeper
        # 2 Allrounder
        

    def createLineup(self):
        eleven = list(self.starting)
        print(len(eleven))
        openers = []
        top_ord = []
        mid_ord = []
        low_ord = []

        for x in eleven:
            if(x.batting_order == "Opener"):
                openers.append(x)
            
            elif(x.batting_order == "Top Order"):
                top_ord.append(x)

            elif(x.batting_order == "Middle Order"):
                mid_ord.append(x)
        
            elif(x.batting_order == "Low Order"):
                low_ord.append(x)
        for x in openers:
            self.lineup.append(x)
        for x in top_ord:
            self.lineup.append(x)
        for x in mid_ord:
            self.lineup.append(x)
        for x in low_ord:
            self.lineup.append(x)
    def printLineup(self):
        for i in range(0, len(self.lineup)):
            print(f'{i+1}. {self.lineup[i].name}')

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


        # elif(openers[0].position == "Allrounder"):
        #                 self.allRounderCount = self.allRounderCount+1
        #                 if(openers[0].bowling_type == "Spinner"):
        #                     self.spinnerCount = self.spinnerCount +1
        #                 else:
        #                     self.pacerCount = self.pacerCount +1
            # wicketkeepers.remove(wicketkeepers[0])
    def evaluateTeam(self):
        # batting_overall
        # bowling_overall
        # fielding_overall

        # opening_rating
        # top_order_rating
        # mid_order_rating
        # low_order_rating
        
        # pace_average
        # spin_average
        
        # wicketkeeper

        
        pass