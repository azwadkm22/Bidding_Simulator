import NameGenerator

from random import randint
import random


def get_random_number(start, end):
    return random.randint(start, end)

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
    if(abs(batting - bowling) < 20 or (batting > 70 and bowling > 70)):
        return "Allrounder"
    elif(batting > bowling):
        if(bowling < 20 and fielding > 70):
            return "Wicketkeeper"
        else:
            return "Batsmen"
    else:
        return "Bowler"

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
        battingWeight = 0.1
        bowlingWeight = 1.5
        fieldingWeight = 0.4
    elif position == "Wicketkeeper":
        battingWeight = 1.4
        fieldingWeight = 0.6
        bowlingWeight = 0
    elif position == "Allrounder":
        battingWeight = .9
        bowlingWeight = .8
        fieldingWeight = 0.3
    
        
    price = int((batting*battingWeight + bowling*bowlingWeight + fielding*fieldingWeight + fame*0.5) * 40)

    return price

class Player():

    def __init__(self):
        self.name = NameGenerator.getPlayerName()
        self.batting = get_random_number(10, 99)
        if(self.batting < 40):
            bowlingLowbound = 50
        else:
            bowlingLowbound = 10
        self.bowling = get_random_number(bowlingLowbound, 99)
        self.fielding = get_random_number(30, 90)
        # self.position = getPosition(self.batting, self.bowling)
        self.position = getPosition(self.batting, self.bowling, self.fielding)
        fameLowbound = max(self.batting-10, self.bowling-10, self.fielding-30, 10)
        self.fame = get_random_number(fameLowbound, 90)

        self.estimated_price = getEstimatedPrice(self.batting, self.bowling, self.fielding, self.fame, self.position)
        
        self.batting_hand = random.choice(["Left", "Right"])

        self.bowling_type = random.choice(["Spinner", "Pacer"])

        self.bowling_style = pickBowlingStyle(self.bowling_type, self.bowling)

        self.batting_order = pickBattingOrder(self.position, self.batting)
        
        # self.traits = findTrait()
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