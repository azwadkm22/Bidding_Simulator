import random

class RandomBidder:
    def __init__(self, name, budget):
        self.category = "Random"
        self.name = name
        self.budget = budget
    
    def placeBid(self, player, running_price):
        if self.budget -running_price < 0:
            return 0
        return random.choice([0, 1])

    def subtractPrice(self, running_price):
        self.budget = self.budget - running_price



class SafeBidder:
    def __init__(self, name, budget):
        self.category = "Random"
        self.name = name
        self.budget = budget
    
    def placeBid(self, player, running_price):
        if self.budget -running_price < 0:
            return 0
        if(player.estimated_price > running_price):
            return 1
        else:
            return 0
    def subtractPrice(self, running_price):
        self.budget = self.budget - running_price


class RiskyBidder:
    def __init__(self, name, budget):
        self.category = "Random"
        self.name = name
        self.budget = budget
    
    def placeBid(self, player, running_price):
        if self.budget -running_price < 0:
            return 0
        if(player.estimated_price > running_price/1.25):
            return 1
        else:
            return 0
        
    def subtractPrice(self, running_price):
        self.budget = self.budget - running_price
    
class AlwaysBidder:
    def __init__(self, name, budget):
        self.category = "Always"
        self.name = name
        self.budget = budget
    
    def placeBid(self, player, running_price):
        if self.budget -running_price < 0:
            return 0
        return 1
    
    def subtractPrice(self, running_price):
        self.budget = self.budget - running_price

    
class NeverBidder:
    def __init__(self, name, budget):
        self.category = "Always"
        self.name = name
        self.budget = budget
    
    def placeBid(self, player, running_price):
        if self.budget -running_price < 0:
            return 0
        return 0
    
    def subtractPrice(self, running_price):
        self.budget = self.budget - running_price