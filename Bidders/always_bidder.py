from base_bidder import BaseBidder

class AlwaysBidder(BaseBidder):
    def __init__(self, name, budget, team):
        super().__init__(name, budget, "Always", team)
    
    def place_bid(self, player, running_price):
        if self.team.number_of_players > 20:
            return 0
        if self.budget - running_price < 0:
            return 0
        return 1