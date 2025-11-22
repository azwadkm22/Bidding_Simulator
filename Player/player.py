
from Player.name_generator.player_name_generator import getPlayerName

from random import randint
from Utils.probability_utils import get_random_normal_distribution_number_biased
import random

class Player():

    def __init__(self, player_id, json_data = None):

        if json_data == None:
            self.player_id = player_id
            self.name = getPlayerName()
            self.batting = get_random_normal_distribution_number_biased(20, 96)
            bowlSkillStart = 20
            if self.batting > 75:
                bowlSkillStart = 10
            elif self.batting < 50:
                bowlSkillStart = 30
            self.bowling = get_random_normal_distribution_number_biased(bowlSkillStart, 96)
            self.fielding = get_random_normal_distribution_number_biased(50, 85, 15)
            self.position = self.getPosition()
            if self.position == "Trainee":
                self.fielding = 45
            fameLowbound = max(self.batting-10, self.bowling-10, self.fielding-30, 10)
            fameHighbound = max(self.batting-5, self.bowling-5, self.fielding-20, 70)
            self.fame = 50#get_random_normal_distribution_number_biased(fameLowbound, fameHighbound)

            self.estimated_price = self.getEstimatedPrice()
            
            self.batting_hand = random.choice(["Left", "Right"])

            self.bowling_type = random.choice(["Spinner", "Pacer"])

            self.bowling_style = self.pickBowlingStyle()

            self.batting_order = self.pickBattingOrder()
            
            self.selling_price = 0
        else:
            self.player_id = player_id
            self.name = json_data["name"]
            self.batting = json_data["batting"]
            self.bowling = json_data["bowling"]
            self.fielding = json_data["fielding"]
            self.position = json_data["position"]
            self.fame = json_data["fame"]
            self.estimated_price = json_data["estimated_price"]
            self.batting_hand = json_data["batting_hand"]
            self.bowling_type = json_data["bowling_type"]
            self.bowling_style = json_data["bowling_style"]
            self.batting_order = json_data["batting_order"]
            self.selling_price = json_data["selling_price"]
 
    def printDetails(self):
        print(self.name)
        print("Batting Skill: ", self.batting)
        print("Bowling Skill: ", self.bowling)
        print("Fielding Skill: ", self.fielding)
        print("Position: ", self.position)
        print("Fame: ", self.fame)
        print("Estimated Price: ", self.estimated_price)
        print("Batting Hand: ", self.batting_hand)
        print("Batting Order: ", self.batting_order)
        print("Bowling Type: ", self.bowling_type)
        print("Bowling Style: ", self.bowling_style)
        print("")

    def setSellingPrice(self, price):
        self.selling_price = price

    def printSkill(self):
        print(self.name)
        print("Batting Skill: ", self.batting)
        print("Bowling Skill: ", self.bowling)
        print("Fielding Skill: ", self.fielding)
        print("")

    def printSummary(self):
        print(self.name)
        print("Position: ", self.position)
        if(self.position == "Batsmen"):
            print("Batting Skill: ", self.batting)
        elif (self.position == "Wicketkeeper"):
            print("Batting Skill: ", self.batting)
            print("Fielding Skill: ", self.fielding)
        elif(self.position == "Bowler"):
            print("Bowling Skill: ", self.bowling)
            print("Bowling Type: ", self.bowling_type)
        else:
            print("Batting Skill: ", self.batting)
            print("Bowling Skill: ", self.bowling)
            print("Bowling Type: ", self.bowling_type)        
        print("Batting Order: ", self.batting_order)
        print("")

    def printPosition(self):
        print(self.name)
        print("Position: ", self.position)
        print("Estimated Price: ", self.estimated_price)

    def printName(self):
        print(self.name)

    def printInLine(self):
        print(f'{self.name}: ', end="")
        if self.position == "Batsmen":
            print(f'BAT({self.batting}) {self.batting_order} Batsmen', end="")
        if self.position == "Wicketkeeper":
            print(f'BAT({self.batting}) Wicketkeeper', end="")
        if self.position == "Bowler":
            if self.bowling_type == "Pacer":
                print(f'BWL({self.bowling}) Pacer', end="")
            else:
                print(f'BWL({self.bowling}) Spinner', end="")
        if self.position == "Allrounder":
            if self.bowling_type == "Pacer":
                print(f'BAT({self.batting}) BWL({self.bowling}) Allrounder Pacer', end="")
            else:
                print(f'BAT({self.batting}) BWL({self.bowling}) Allrounder Spinner', end="")

        if self.selling_price != 0:
            print(f' Sold At:{self.selling_price}', end="")

        print(f', Est: {self.estimated_price}')

    def getPosition(self):
        if self.batting < 50 and self.bowling < 50:
            return "Trainee"
        
        if((abs(self.batting - self.bowling) < 10 and self.batting > 60) or (self.batting > 75 and self.bowling > 70)):
            return "Allrounder"
        elif(self.batting > self.bowling):
            if(self.bowling < 40 and self.fielding > 75):
                return "Wicketkeeper"
            elif (self.batting - self.bowling > 30 and self.fielding > 70 and self.batting > 80):
                return "Wicketkeeper"
            else:
                return "Batsmen"
        elif self.bowling > self.batting:
            return "Bowler"
        else:
            return "Trainee"
        
    def pickBowlingStyle(self):
        if self.bowling_type == "Spinner":
            return random.choice(["Off-Spin", "Leg-Spin", "Left-arm orthodox spin", "Left-arm unorthodox spin"])
        else:
            if(self.bowling > 95):
                return "Fast"
            elif(self.bowling > 90):
                return random.choice(["Fast", "Fast-medium"])
            elif(self.bowling > 80):
                return random.choice(["Fast", "Fast-medium", "Medium"])
            elif(self.bowling > 70):
                return random.choice(["Fast-medium", "Medium", "Slow"])
            else:
                return random.choice(["Medium", "Slow"])

    def pickBattingOrder(self):
        if self.position == "Bowler":
            return "Low Order"
        
        roll = random.randint(0, 100)
        if(roll > 75):
            return "Opener"
        elif(roll > 45):
            return "Top Order"
        elif(roll > 15):
            return "Middle Order"
        else:
            return "Low Order"

    def getEstimatedPrice(self):
        batting = (self.batting - 10) / (99 - 10)
        bowling = (self.bowling - 10) / (99 - 10)
        fielding = (self.fielding - 30) / (90 - 30)
        fame = (self.fame - 10) / (90 - 10)

        fameWeight = 0.5
        fieldingWeight = 0.5
        battingWeight = 0.5
        bowlingWeight = 0.5
        # Batting + Bowling + Fielding = 2
        if self.position == "Batsmen":
            battingWeight = 1.8
            fieldingWeight = 0.2
            bowlingWeight = 0
        elif self.position == "Bowler":
            battingWeight = 0
            bowlingWeight = 1.8
            fieldingWeight = 0.2
        elif self.position == "Wicketkeeper":
            battingWeight = 1.7
            fieldingWeight = 0.3
            bowlingWeight = 0
        elif self.position == "Allrounder":
            battingWeight = .9
            bowlingWeight = .8
            fieldingWeight = 0.2
        
            
        price = int((batting*battingWeight + bowling*bowlingWeight + fielding*fieldingWeight) * 40) * 2

        return price
    
    def get_JSON_data(self):
        return {
            "name": self.name,
            "batting": self.batting,
            "bowling": self.bowling,
            "fielding": self.fielding,
            "position": self.position,
            "fame": self.fame,
            "estimated_price": self.estimated_price,
            "batting_hand": self.batting_hand,
            "bowling_type": self.bowling_type,
            "bowling_style": self.bowling_style,
            "batting_order": self.batting_order,
            "selling_price": self.selling_price
        }
        


# lowestEP = 1000000
# # lowPlayer = 1
# highPlayer = 1

# ALLSTARS = []
# for j in range(10):

#     highestEP = -1
#     for i in range(100):
#         a = Player()
#         # if(a.estimated_price < lowestEP):
#         #     lowestEP  = a.estimated_price
#         #     lowPlayer = a

#         if(a.estimated_price > highestEP):
#             highestEP = a.estimated_price
#             highPlayer = a
#     # highPlayer.printDetails()
#     ALLSTARS.append(highPlayer)


# for p in ALLSTARS:
#     p.printDetails()
#     print()


# getPerson()



# for i in first:
# 	for j in last:
# 		print(i, j)