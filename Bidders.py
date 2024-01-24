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
            return random.choice([0, 1, 1, 1])
        else:
            return 0
        

class SpecializedBidder(BaseBidder):
    def __init__(self, name, budget, team, focus):
        super().__init__(name, budget, "Specialized", team)
        self.focus = focus
    def placeBid(self, player, running_price):
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
        


class SpecialBidder(BaseBidder):
    def __init__(self, name, budget, team, focus):
        super().__init__(name, budget, "Specialized", team)
        self.focus = focus
    def placeBid(self, player, running_price):
        if self.team.number_of_players > 20:
            return 0
        if self.budget - running_price < 0:
            return 0
        
        priority = self.team.findNewPlayerPriority(player)
        # if priority == 0:
        #     return 0
        # else:
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