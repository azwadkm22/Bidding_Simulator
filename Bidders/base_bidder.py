from base_bidder import BaseBidder

class BaseBidder:
    def __init__(self, name, budget, category, team):
        self.category = category
        self.name = name
        self.budget = budget
        self.team = team
    
    def place_bid(self, player, running_price):
        raise NotImplementedError("Subclasses must implement the placeBid method.")
    
    def subtract_price(self, running_price):
        self.budget = self.budget - running_price
    
    def add_player_to_team(self, player):
        self.team.add_player(player)