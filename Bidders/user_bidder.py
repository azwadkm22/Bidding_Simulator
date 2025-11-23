from Utils.probability_utils import get_probabilistic_answer
from Team.team import Team

# Utility will be a function of players position
class UserBidder:

    def __init__(self, name, budget, team: Team):
        self.budget = budget
        self.team = team
        self.utility = 0
        self.name = name
        self.playerUtility = 0


    def placeBid(self, player, running_price):
        
        if self.team.number_of_players > 20:
            return 0
        utility = self.calculate_utility(player, running_price)
        if utility < 0:
            return 0
        elif utility > 1:
            return 1
        else:
            return get_probabilistic_answer(utility)
    
    def subtractPrice(self, running_price):
        self.budget = self.budget - running_price
    
    def addPlayerToTeam(self, player):
        self.team.addPlayer(player)

