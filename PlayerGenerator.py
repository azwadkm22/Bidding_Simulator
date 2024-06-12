import NameGenerator
from random import randint
from ProbabilisticFunctionsModule import get_random_normal_distribution_number_biased
import random


# def get_random_normal_distribution_number_biased(start, end):
#     return random.gauss(mu, sigma)

# get_random_normal_distribution_number_biased(0, 99)
# check_distribution(10, 99)


def pickBowlingStyle(bowling_type, bowling):
    if bowling_type == "Spinner":
        return random.choice(["Off-Spin", "Leg-Spin", "Left-arm orthodox spin", "Left-arm unorthodox spin"])
    else:
        if(bowling > 95):
            return "Fast"
        elif(bowling > 90):
            return random.choice(["Fast", "Fast-medium"])
        elif(bowling > 80):
            return random.choice(["Fast", "Fast-medium", "Medium"])
        elif(bowling > 70):
            return random.choice(["Fast-medium", "Medium", "Slow"])
        else:
            return random.choice(["Medium", "Slow"])

def pickBattingOrder(position, batting):
    if position == "Bowler":
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


    
def getPosition(batting, bowling, fielding):

    if batting < 50 and bowling < 50:
        return "Trainee"
    
    if((abs(batting - bowling) < 10 and batting > 60) or (batting > 75 and bowling > 70)):
        return "Allrounder"
    elif(batting > bowling):
        if(bowling < 50 and fielding > 75):
            return "Wicketkeeper"
        elif (batting - bowling > 30 and fielding > 70 and batting > 80):
            return "Wicketkeeper"
        else:
            return "Batsmen"
    elif bowling > batting:
        return "Bowler"
    else:
        return "Trainee"

def getEstimatedPrice(batting, bowling, fielding, fame, position):

    batting = (batting - 10) / (99 - 10)
    bowling = (bowling - 10) / (99 - 10)
    fielding = (fielding - 30) / (90 - 30)
    fame = (fame - 10) / (90 - 10)

    fameWeight = 0.5
    fieldingWeight = 0.5
    battingWeight = 0.5
    bowlingWeight = 0.5
    # Batting + Bowling + Fielding = 2
    if position == "Batsmen":
        battingWeight = 1.5
        fieldingWeight = 0.5
        bowlingWeight = 0
    elif position == "Bowler":
        battingWeight = 0
        bowlingWeight = 1.6
        fieldingWeight = 0.4
    elif position == "Wicketkeeper":
        battingWeight = 1.4
        fieldingWeight = 0.6
        bowlingWeight = 0
    elif position == "Allrounder":
        battingWeight = .9
        bowlingWeight = .8
        fieldingWeight = 0.3
    
        
    price = int((batting*battingWeight + bowling*bowlingWeight + fielding*fieldingWeight + fame*0.5) * 40) * 2

    return price

class Player():
    """

    """
    # def __init__(self, name, batting, bowling, fielding, position, fame, batting_hand, bowling_type, bowling_style, batting_order):
    #     self.name = name
    #     self.batting = batting
    #     self.bowling = bowling
    #     self.fielding = fielding
    #     self.position = position
    #     self.fame = fame
    #     self.estimated_price = getEstimatedPrice(self.batting, self.bowling, self.fielding, self.fame, self.position)
    #     self.batting_hand = batting_hand

    #     self.bowling_type = bowling_type

    #     self.bowling_style = bowling_style
    #     self.batting_order = batting_order
    #     self.selling_price = 0
      
    def __init__(self):
        self.name = NameGenerator.getPlayerName()
        self.batting = get_random_normal_distribution_number_biased(20, 96)
        self.bowling = get_random_normal_distribution_number_biased(20, 96)
        self.fielding = get_random_normal_distribution_number_biased(45, 96)
        self.position = getPosition(self.batting, self.bowling, self.fielding)
        if self.position == "Trainee":
            self.fielding = 45
        fameLowbound = max(self.batting-10, self.bowling-10, self.fielding-30, 10)
        fameHighbound = max(self.batting-5, self.bowling-5, self.fielding-20, 70)
        self.fame = 50#get_random_normal_distribution_number_biased(fameLowbound, fameHighbound)

        self.estimated_price = getEstimatedPrice(self.batting, self.bowling, self.fielding, self.fame, self.position)
        
        self.batting_hand = random.choice(["Left", "Right"])

        self.bowling_type = random.choice(["Spinner", "Pacer"])

        self.bowling_style = pickBowlingStyle(self.bowling_type, self.bowling)

        self.batting_order = pickBattingOrder(self.position, self.batting)
        
        self.selling_price = 0
 
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