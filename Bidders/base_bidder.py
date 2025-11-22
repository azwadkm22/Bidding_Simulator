from base_bidder import BaseBidder

class BaseBidder:
    def __init__(self, name, budget, category, team):
        self.category = category
        self.name = name
        self.budget = budget
        self.team = team
    
    def placeBid(self, player, running_price):
        raise NotImplementedError("Subclasses must implement the placeBid method.")
    
    def subtractPrice(self, running_price):
        self.budget = self.budget - running_price
    
    def addPlayerToTeam(self, player):
        self.team.addPlayer(player)