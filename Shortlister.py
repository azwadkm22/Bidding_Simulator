import random
from PlayerGenerator import Player


# 4 Bastsmen above 80
# 2 Spinners above 80
# 2 Pacers above 80
# 2 Allrounders above 80
# 1 Wicketkeeper above 75
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
        for player in self.players:
            player.printSummary()
    

def getProbabilisticAnswer(probability):
    # Generate a random number between 0 and 1
    random_number = random.random()
    
    # Check if the random number is less than the given probability
    if random_number < probability:
        return 1  # Return 1 if the condition is met
    else:
        return 0  # Return 0 otherwise


def makeShortList(playerList, teamNames):
    teamShortList = {}
    for team in teamNames:
        teamShortList[team] = ShortList()
    
    while(len(playerList) > 0):
        player = random.choice(playerList)
        playerList.remove(player)
        if player.position == "Batsmen":
            for shortList in teamShortList:
                yes = getProbabilisticAnswer( (4 - teamShortList[shortList].batCount) *.15)
                if yes == 1:
                    teamShortList[shortList].shortListPlayer(player)
                
        
        if player.position == "Wicketkeeper":
            for shortList in teamShortList:
                yes = getProbabilisticAnswer( (1 - teamShortList[shortList].wicketKeeperCount) *.5)
                if yes == 1:
                    teamShortList[shortList].shortListPlayer(player)
                
        
        if player.position == "Allrounder":
            for shortList in teamShortList:
                yes = getProbabilisticAnswer( (2 - teamShortList[shortList].allRounderCount) *.3)
                if yes == 1:
                    teamShortList[shortList].shortListPlayer(player)
        
        if player.position == "Bowler":
            if player.bowling_type == 'Spinner':
                for shortList in teamShortList:
                    yes = getProbabilisticAnswer( (2 - teamShortList[shortList].spinnerCount) *.3)
                    if yes == 1:
                        teamShortList[shortList].shortListPlayer(player)
            else:
                for shortList in teamShortList:
                    yes = getProbabilisticAnswer( (2 - teamShortList[shortList].pacerCount) *.3)
                    if yes == 1:
                        teamShortList[shortList].shortListPlayer(player)
        
    for team in teamNames:
        print()
        print()
        print(f"Shortlist of {team}")
        print()
        print()
        teamShortList[team].printShortList()
        
    print(playerList)
    return teamShortList