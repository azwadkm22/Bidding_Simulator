from base_bidder import BaseBidder

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
            return random.choice([0, 1, 1, 1])
        else:
            return 0