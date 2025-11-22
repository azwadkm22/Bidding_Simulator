import random
from base_bidder import BaseBidder

class SpecializedBidder(BaseBidder):
    def __init__(self, name, budget, team, focus):
        super().__init__(name, budget, "Specialized", team)
        self.focus = focus
    def place_bid(self, player, running_price):
        if self.team.number_of_players > 20:
            return 0
        if self.budget - running_price < 0:
            return 0
        addition = 0
        if(self.focus == "Batting"):
            if(player.batting > self.team.batting_average):
                addition = 1
            if(player.batting > 80):
                addition = 2
            if(player.batting > 90):
                addition = 4
            if(player.batting > 95):
                addition = 5
        elif(self.focus == "Bowling"):
            if(player.bowling > self.team.bowling_average):
                addition = 1
            if(player.bowling > 80):
                addition = 2
            if(player.bowling > 90):
                addition = 4
            if(player.bowling > 95):
                addition = 5
        elif(self.focus == "Spin"):
            if(player.bowling_type == "Spinner" and player.bowling > self.team.spin_bowling_average):
                addition = 1
            if(player.bowling > 80):
                addition = 2
            if(player.bowling > 90):
                addition = 4
            if(player.bowling > 95):
                addition = 5
        elif(self.focus == "Pace"):
            if(player.bowling_type == "Pacer" and player.bowling > self.team.pace_bowling_average):
                addition = 1
            if(player.bowling > 80):
                addition = 2
            if(player.bowling > 90):
                addition = 4
            if(player.bowling > 95):
                addition = 5
        priority = self.team.findNewPlayerPriority(player)
        if priority == 0:
            return 0
        if player.estimated_price > running_price / (1+(priority/10)+addition/5):
            return random.choice([0, 1, 1, 1])
        else:
            return 0