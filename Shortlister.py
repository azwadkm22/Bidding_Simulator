import random
from PlayerGenerator import Player
from ProbabilisticFunctionsModule import getProbabilisticAnswer

class ShortList:
    def __init__(self):
        self.players = set()
        self.batCount = 0
        self.bowlCount = 0
        self.spinnerCount = 0
        self.pacerCount = 0
        self.allRounderCount = 0
        self.wicketKeeperCount = 0
        self.estimatedCost = 0
    
    def shortListPlayer(self, player):
        self.players.add(player)
        
        self.estimatedCost = self.estimatedCost + player.estimated_price
        
        if player.position == "Batsmen":
            self.batCount = self.batCount + 1
            pass
        
        if player.position == "Wicketkeeper":
            self.wicketKeeperCount = self.wicketKeeperCount + 1
            pass
        
        if player.position == "Allrounder":
            self.allRounderCount = self.allRounderCount + 1
            if player.bowling_type == 'Spinner':
                self.spinnerCount = self.spinnerCount + 1
            else:
                self.pacerCount = self.pacerCount + 1
        
        if player.position == "Bowler":
            self.bowlCount = self.bowlCount + 1
            if player.bowling_type == 'Spinner':
                self.spinnerCount = self.spinnerCount + 1
            else:
                self.pacerCount = self.pacerCount + 1
    
    def getShortlistedPlayers(self):
        return self.players
    
    def printShortList(self):

        

        print("Shortlisted Batsmen: ", self.batCount)
        print("Shortlisted Bowler: ", self.bowlCount)
        print("Shortlisted Spinner: ", self.spinnerCount)
        print("Shortlisted Pacer: ", self.pacerCount)
        print("Shortlisted Allrounder: ", self.allRounderCount)
        print("Shortlisted WicketKeeper: ", self.wicketKeeperCount)
        print("Shortlisted Estimated Cost: ", self.estimatedCost)


        for player in self.players:
            player.printSummary()
        
        
    




def makeShortList(playerList, teamNames, estimatedCostMax=3000):
    teamShortList = {}
    cost = 0
    for player in playerList:
        cost = cost + player.estimated_price
    
    estimatedCostMax = (cost / len(playerList)) * 15
    print(estimatedCostMax)
    rivalsForPlayers = {}
    for team in teamNames:
        teamShortList[team] = ShortList()
    
    while(len(playerList) > 0):
        player = random.choice(playerList)
        rivalsForPlayers[player] = set()
        if player.position == "Batsmen":
            for shortList in teamShortList:
                if teamShortList[shortList].estimatedCost < estimatedCostMax:
                    battingDependentProbability = 0.15
                    if player.batting >= 95: 
                        battingDependentProbability = .30
                    elif player.batting >= 90: 
                        battingDependentProbability = .25
                    elif player.batting >= 85: 
                        battingDependentProbability = .20
                    yes = getProbabilisticAnswer( (4 - teamShortList[shortList].batCount) * battingDependentProbability)
                    if yes == 1:
                        teamShortList[shortList].shortListPlayer(player)
                        if player in playerList:
                            playerList.remove(player)
        
        elif player.position == "Wicketkeeper":
            for shortList in teamShortList:
                if teamShortList[shortList].estimatedCost < estimatedCostMax:
                    battingDependentProbability = 0.35
                    if player.batting >= 90: 
                        battingDependentProbability = .5
                    elif player.batting >= 85: 
                        battingDependentProbability = 0.45
                    yes = getProbabilisticAnswer( (2 - teamShortList[shortList].wicketKeeperCount) * battingDependentProbability)
                    if yes == 1:
                        teamShortList[shortList].shortListPlayer(player)
                        if player in playerList:
                            playerList.remove(player)
                    
        
        elif player.position == "Allrounder":
            for shortList in teamShortList:
                if teamShortList[shortList].estimatedCost < estimatedCostMax:
                    avgDependentProbability = 0.25
                    if (player.batting + player.bowling)/2 >= 90 or max(player.batting, player.bowling) >= 90 : 
                        avgDependentProbability = .4
                    elif (player.batting + player.bowling)/2 >= 85 or max(player.batting, player.bowling) >= 85: 
                        avgDependentProbability = .3
                    yes = getProbabilisticAnswer( (3 - teamShortList[shortList].allRounderCount) * avgDependentProbability)
                    if yes == 1:
                        teamShortList[shortList].shortListPlayer(player)
                        if player in playerList:
                            playerList.remove(player)
        
        elif player.position == "Bowler":
            bowlerDependentProbability = 0.20
            if player.bowling >= 95: 
                bowlerDependentProbability = .4
            elif player.bowling >= 90: 
                bowlerDependentProbability = .3
            elif player.bowling >= 85: 
                bowlerDependentProbability = .25
            if player.bowling_type == 'Spinner':
                for shortList in teamShortList:
                    if teamShortList[shortList].estimatedCost < estimatedCostMax:
                        yes = getProbabilisticAnswer( (4 - teamShortList[shortList].spinnerCount) * bowlerDependentProbability)
                        if yes == 1:
                            teamShortList[shortList].shortListPlayer(player)
                            if player in playerList:
                                playerList.remove(player)
            else:
                for shortList in teamShortList:
                    if teamShortList[shortList].estimatedCost < estimatedCostMax:
                        yes = getProbabilisticAnswer( (4 - teamShortList[shortList].pacerCount) * bowlerDependentProbability)
                        if yes == 1:
                            teamShortList[shortList].shortListPlayer(player)
                            if player in playerList:
                                playerList.remove(player)

        if player in playerList:
            for shortList in teamShortList:
                # if teamShortList[shortList].estimatedCost < estimatedCostMax:
                    maxDependentProbability = 0.05
                    if max(player.batting, player.bowling) >= 95:
                        maxDependentProbability = 0.45
                    elif max(player.batting, player.bowling) >= 90:
                        maxDependentProbability = 0.35
                    elif max(player.batting, player.bowling) >= 85:
                        maxDependentProbability = 0.15
                    yes = getProbabilisticAnswer(maxDependentProbability)
                    if yes == 1:
                        teamShortList[shortList].shortListPlayer(player)
                        if player in playerList:
                            playerList.remove(player)

        for team in teamShortList:
            if player in teamShortList[team].players:
                rivalsForPlayers[player].add(team)
        # print(playerList)
        

    return teamShortList, rivalsForPlayers