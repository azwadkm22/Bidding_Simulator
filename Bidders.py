import random

class RandomBidder:
    def __init__(self, name):
        self.category = "Random"
        self.name = name
    
    def placeBid(self):
        return random.choice([0, 0, 0, 1])

    
class AlwaysBidder:
    def __init__(self, name):
        self.category = "Always"
        self.name = name
    
    def placeBid(self):
        return 1

    
class NeverBidder:
    def __init__(self, name):
        self.category = "Always"
        self.name = name
    
    def placeBid(self):
        return 0