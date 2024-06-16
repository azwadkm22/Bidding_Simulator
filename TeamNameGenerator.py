import random
from ProbabilisticFunctionsModule import getProbabilisticAnswer

Regions = [
    "Dhaka", 
    "Rajshahi", 
    "Sylhet", 
    "Barishal", 
    "Khulna", 
    "Cumilla", 
    "Noakhali", 
    "Chittagong", 
    "Dinajpur", 
    "Jessore", 
    "Mymensingh", 
    "Rangpur",
    "Bogura"
]

EndNames= [
    "Dynamites",
    "Bulls",
    "Titans",
    "Tigers",
    "Sixers",
    "Howlers",
    "Wolves",
    "Gladiators",
    "Riders",
    "Victorians",
    "Kings",
    "Rajahs",
    "Vipers",
    "Dragons"
]

StartNames = [
    "Stellar",
    "Royal",
    "Mighty",
    "Ferocious"

]

def createTeamName():
    # print(len(Regions), len(StartNames), len(EndNames))
    reg = random.choice(Regions)
    Regions.remove(reg)

    if len(StartNames) > 0:
        if(getProbabilisticAnswer(0.2)):
            start = random.choice(StartNames)
            StartNames.remove(start)
            return start + " " + reg

    end = random.choice(EndNames)
    EndNames.remove(end)
    return reg + " " + end
        

# for i in range(10):
#     print(createTeamName())
#     