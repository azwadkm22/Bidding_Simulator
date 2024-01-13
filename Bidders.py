import random

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
    

class RandomBidder(BaseBidder):
    def __init__(self, name, budget, team):
        super().__init__(name, budget, "Random", team)
    
    def placeBid(self, player, running_price):
        if self.budget - running_price < 0:
            return 0
        if self.team.number_of_players > 20:
            return 0
        return random.choice([0, 1])

class SafeBidder(BaseBidder):
    def __init__(self, name, budget, team):
        super().__init__(name, budget, "Safe", team)
    
    def placeBid(self, player, running_price):
        if self.team.number_of_players > 20:
            return 0
        if self.budget - running_price < 0:
            return 0
        if player.estimated_price > running_price:
            return 1
        else:
            return 0

class RiskyBidder(BaseBidder):
    def __init__(self, name, budget, team):
        super().__init__(name, budget, "Risky", team)
    
    def placeBid(self, player, running_price):
        if self.team.number_of_players > 20:
            return 0
        if self.budget - running_price < 0:
            return 0
        if player.estimated_price > running_price / 1.25:
            return 1
        else:
            return 0

class AlwaysBidder(BaseBidder):
    def __init__(self, name, budget, team):
        super().__init__(name, budget, "Always", team)
    
    def placeBid(self, player, running_price):
        if self.team.number_of_players > 20:
            return 0
        if self.budget - running_price < 0:
            return 0
        return 1

class NeverBidder(BaseBidder):
    def __init__(self, name, budget, team):
        super().__init__(name, budget, "Never", team)
    
    def placeBid(self, player, running_price):
        if self.team.number_of_players > 20:
            return 0
        if self.budget - running_price < 0:
            return 0
        return 0

class PriorityBidder(BaseBidder):
    def __init__(self, name, budget, team):
        super().__init__(name, budget, "Priority", team)
    
    def placeBid(self, player, running_price):
        if self.team.number_of_players > 20:
            return 0
        if self.budget - running_price < 0:
            return 0
        
        priority = self.team.findNewPlayerPriority(player)
        if priority == 0:
            return 0
        if player.estimated_price > running_price / (1+(priority/10)):
            return 1
        else:
            return 0