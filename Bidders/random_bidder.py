from base_bidder import BaseBidder
import random

class RandomBidder(BaseBidder):
    def __init__(self, name, budget, team):
        super().__init__(name, budget, "Random", team)
    
    def placeBid(self, player, running_price):
        if self.budget - running_price < 0:
            return 0
        if self.team.number_of_players > 20:
            return 0
        return random.choice([0, 1])