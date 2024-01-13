import random

class RandomBidder:
    def __init__(self, name):
        self.category = "Random"
        self.name = name
    
    def placeBid(self, player, running_price):
        return random.choice([0, 1])



class SafeBidder:
    def __init__(self, name):
        self.category = "Random"
        self.name = name
    
    def placeBid(self, player, running_price):
        if(player.estimated_price > running_price):
            return 1
        else:
            return 0

class RiskyBidder:
    def __init__(self, name):
        self.category = "Random"
        self.name = name
    
    def placeBid(self, player, running_price):
        if(player.estimated_price > running_price/2):
            return 1
        else:
            return 0
    
class AlwaysBidder:
    def __init__(self, name):
        self.category = "Always"
        self.name = name
    
    def placeBid(self, player, running_price):
        return 1

    
class NeverBidder:
    def __init__(self, name):
        self.category = "Always"
        self.name = name
    
    def placeBid(self, player, running_price):
        return 0