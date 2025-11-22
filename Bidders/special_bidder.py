import random
from base_bidder import BaseBidder

class SpecialBidder(BaseBidder):
    def __init__(self, name, budget, team, focus):
        super().__init__(name, budget, "Specialized", team)
        self.focus = focus
    def place_bid(self, player, running_price):
        if self.team.number_of_players > 20:
            return 0
        if self.budget - running_price < 0:
            return 0
        
        choices = [0, 0, 0, 0, 0, 0, 0, 1]
        if(player.fame > 70):
            choices.append(1)
        if(player.fame > 80):
            choices.append(1)
        if(player.fame > 90):
            choices.append(1)
        if(player.position == "Batsman" and player.batting<60):
            choices.append(0)
        if(player.position == "Batsman" and player.batting<50):
            choices.append(0)
        if(player.position == "Batsman" and player.batting>70):
            choices.append(1)
        if(player.position == "Batsman" and player.batting>80):
            choices.append(1)
        if(player.position == "Batsman" and player.batting>90):
            choices.append(1)


        if(player.position == "Bowler" and player.bowling<60):
            choices.append(0)
        if(player.position == "Bowler" and player.bowling<50):
            choices.append(0)
        if(player.position == "Bowler" and player.bowling>70):
            choices.append(1)
        if(player.position == "Bowler" and player.bowling>80):
            choices.append(1)
        if(player.position == "Bowler" and player.bowling>90):
            choices.append(1)
        
        if(player.position == "Allrounder" and player.bowling<60 and player.batting<60):
            choices.append(0)
        
        if(player.position == "Wicketkeeper" and player.batting>70 and self.team.number_of_wicketkeepers < 1):
            choices.append(1)
        if(player.position == "Wicketkeeper" and player.batting>80 and self.team.number_of_wicketkeepers < 2):
            choices.append(1)
        if(player.position == "Wicketkeeper" and player.batting>90 and self.team.number_of_wicketkeepers < 3):
            choices.append(1)
            
        if running_price > player.estimated_price:
            choices.append(0)
        if running_price > 1.1*player.estimated_price:
            choices.append(0)
            choices.append(0)
            choices.append(0)
        if running_price > 1.2*player.estimated_price:
            choices.append(0)
            choices.append(0)
        if running_price > 1.3*player.estimated_price:
            choices.append(0)
            choices.append(0)
            choices.append(0)
        if running_price > 1.4*player.estimated_price:
            choices.append(0)
            choices.append(0)
            choices.append(0)
            choices.append(0)
        if running_price > 1.5*player.estimated_price:
            choices = [0]
        
        # if player.estimated_price > running_price:
        return random.choice(choices)
        # else:
        #     return 0