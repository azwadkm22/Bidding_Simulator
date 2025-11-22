import time
import random
from TeamNameGenerator import createTeamName
from TeamStrength import findTeamStrength
from Player.player import Player
from Team import Team, printTeamPositionAndOrderDetails, printTeamPositionAndOrderSummary
from StartingEleven import StartingEleven
from Shortlister import ShortList, makeShortList
from Bidders.utility_based_bidder import UtilityBasedBidder

def GenerateNPlayerList(n):
    ListOfPlayers = []

    for i in range(n):
        NewPlayer = Player()
        ListOfPlayers.append(NewPlayer)
    return ListOfPlayers

def getPlayerSubset(playerList, role):
    subList = []
    if role == "Opener":
        for player in playerList:
            if player.batting_order == "Opener":
                subList.append(player)
        return subList
    
    elif role == "Wicketkeeper":
        for player in playerList:
            if player.position == "Wicketkeeper":
                subList.append(player)
        return subList
    
    elif role == "Allrounder":
        for player in playerList:
            if player.position == "Allrounder":
                subList.append(player)
        return subList
    
    elif role == "Spinner":
        for player in playerList:
            if (player.position == "Bowler" or player.position == "Allrounder") and player.bowling_type == "Spinner":
                subList.append(player)
        return subList

    elif role == "Pacer":
        for player in playerList:
            if (player.position == "Bowler" or player.position == "Allrounder") and player.bowling_type == "Pacer":
                subList.append(player)
        return subList
    return subList
        

def FindTopNPlayerInCategory(playerList, n, category):
    # One case left to handle what if n is bigger than sublist
    if(category == "Fame"):
        playerList = sorted(playerList, key=lambda Player: Player.fame, reverse=True)
        TopNPlayers = playerList[:n]
        return TopNPlayers

    elif(category == "Batting"):
        playerList = sorted(playerList, key=lambda Player: Player.batting, reverse=True)
        TopNPlayers = playerList[:n]
        return TopNPlayers
    
    elif(category == "Bowling"):
        playerList = sorted(playerList, key=lambda Player: Player.bowling, reverse=True)
        TopNPlayers = playerList[:n]
        return TopNPlayers
    
    elif(category == "Price"):
        playerList = sorted(playerList, key=lambda Player: Player.estimated_price, reverse=True)
        TopNPlayers = playerList[:n]
        return TopNPlayers
    
    elif(category == "Pacer"):
        subList = getPlayerSubset(playerList, "Pacer")
        subList = sorted(subList, key=lambda Player: Player.bowling, reverse=True)
        TopNPlayers = subList[:n]
        return TopNPlayers
    
    elif(category == "Spinner"):
        subList = getPlayerSubset(playerList, "Spinner")
        subList = sorted(subList, key=lambda Player: Player.bowling, reverse=True)
        TopNPlayers = subList[:n]
        return TopNPlayers
    
    elif(category == "Wicketkeeper"):
        subList =  getPlayerSubset(playerList, "Wicketkeeper")
        subList = sorted(subList, key=lambda Player: Player.batting, reverse=True)
        TopNPlayers = subList[:n]
        return TopNPlayers

    elif(category == "Allrounder"):
        subList =  getPlayerSubset(playerList, "Allrounder")
        subList = sorted(subList, key=lambda Player: (Player.batting + Player.bowling )/2, reverse=True)
        TopNPlayers = subList[:n]
        return TopNPlayers
    
    elif(category == "Opener"):
        subList =  getPlayerSubset(playerList, "Opener")
        subList = sorted(subList, key=lambda Player: Player.batting, reverse=True)
        TopNPlayers = subList[:n]
        return TopNPlayers

def FindPlayersWithStatsAbove(playerList, stat, value):
    lop = []
    for player in playerList:
        if(stat == "Batting"):
            if player.batting > value:
                lop.append(player)

        elif(stat == "Bowling"):
            if player.bowling > value:
                lop.append(player)

        elif(stat == "Allrounder"):
            if (player.batting + player.bowling)/2 > value:
                lop.append(player)

        elif(stat == "Spin"):
            if player.bowling > value and player.bowling_type == "Spinner":
                lop.append(player)

        elif(stat == "Pace"):
            if player.bowling > value and player.bowling_type == "Pacer":
                lop.append(player)
    return lop


ListOfPlayers = GenerateNPlayerList(250)
print(ListOfPlayers)
input()
TopTenBatsmen = FindTopNPlayerInCategory(ListOfPlayers, 10, "Batting")
TopTenBowlers = FindTopNPlayerInCategory(ListOfPlayers, 10, "Bowling")
TopTenSpinners = FindTopNPlayerInCategory(ListOfPlayers, 10, "Spinner")
TopTenPacers = FindTopNPlayerInCategory(ListOfPlayers, 10, "Pacer")
TopEightWicketkeepers = FindTopNPlayerInCategory(ListOfPlayers, 24, "Wicketkeeper")
TopTenOpeners = FindTopNPlayerInCategory(ListOfPlayers, 10, "Opener")
TopTenAllrounders = FindTopNPlayerInCategory(ListOfPlayers, 10, "Allrounder")
TopTenFamous = FindTopNPlayerInCategory(ListOfPlayers, 10, "Fame")
TopTenMostExpensive = FindTopNPlayerInCategory(ListOfPlayers, 10, "Price")


ListOfPlayers = sorted(ListOfPlayers, key=lambda Player: Player.estimated_price, reverse=True)

PlayersAbove80Batting = FindPlayersWithStatsAbove(ListOfPlayers, "Batting", 80)
PlayersAbove80Bowling = FindPlayersWithStatsAbove(ListOfPlayers, "Bowling", 80)
PlayersAbove80Spin = FindPlayersWithStatsAbove(ListOfPlayers, "Spin", 80)
PlayersAbove80Pace = FindPlayersWithStatsAbove(ListOfPlayers, "Pace", 80)
PlayersAbove80Allrounder = FindPlayersWithStatsAbove(ListOfPlayers, "Allrounder", 80)

def findPlayersAbove80(playerList):
    playersAbove80 = set()
    for player in playerList:
        if player.batting > 80 or player.bowling > 80:
            playersAbove80.add(player)

    return playersAbove80

def findPlayersAbove90(playerList):
    playersAbove90 = set()
    for player in playerList:
        if player.batting > 90 or player.bowling > 90:
            playersAbove90.add(player)

    return playersAbove90

PlayersAbove80 = findPlayersAbove80(ListOfPlayers)
PlayersAbove80 = sorted(PlayersAbove80, key=lambda Player: max(Player.batting, Player.bowling), reverse=True)
PlayersAbove90 = findPlayersAbove90(ListOfPlayers)

print(len(ListOfPlayers))

for p in ListOfPlayers:
    p.printInLine()
input()


def PrintTitleBoard(Title):
    print("########")
    print("")
    print(Title)
    print("")
    print("########")


def printSummaryOfGeneration():
    PrintTitleBoard("Best Wicketkeepers")
    for pl in TopEightWicketkeepers:
        pl.printSkill()
    input()
    PrintTitleBoard("Best Batsmen")
    for pl in TopTenBatsmen:
        pl.printSummary()
    PrintTitleBoard("Best Bowlers")
    for pl in TopTenBowlers:
        pl.printSummary()
    PrintTitleBoard("Best Allrounders")
    for pl in TopTenAllrounders:
        pl.printSummary()
    
    PrintTitleBoard("Best Openers")
    for pl in TopTenOpeners:
        pl.printSummary()
    PrintTitleBoard("Best Spinners")
    for pl in TopTenSpinners:
        pl.printSummary()
    PrintTitleBoard("Best Pacers")
    for pl in TopTenPacers:
        pl.printSummary()
    PrintTitleBoard("Most Famous")
    for pl in TopTenFamous:
        pl.printSummary()
    PrintTitleBoard("Most Expensive")
    for pl in TopTenMostExpensive:
        pl.printSummary()
    
    PrintTitleBoard("Now all the best players with score above 80")

    listToPrint = [PlayersAbove80Batting, PlayersAbove80Bowling, PlayersAbove80Allrounder, PlayersAbove80Spin, PlayersAbove80Pace]
    setList = set()
    for lst in listToPrint:
        for player in lst:
            setList.add(player)
            player.printInLine()

    print("Total Players above 80: ", len(setList))
    

def countRatio(playerList):
    total = len(playerList)
    bat = 0
    bowl = 0
    spin = 0
    pace = 0
    wk = 0
    allr = 0
    trainee = 0
    for player in playerList:
        if player.position == "Batsmen":
            bat = bat + 1
        elif player.position == "Wicketkeeper":
            wk = wk + 1
        elif player.position == "Allrounder":
            allr = allr + 1
        elif player.position == "Bowler":
            bowl = bowl + 1
            if player.bowling_type == "Spinner":
                spin = spin + 1
            if player.bowling_type == "Pacer":
                pace = pace + 1
        else:
            player.printSkill()
            trainee = trainee + 1

    print("Batsmen Count: ", bat)
    print("Wicketkeeper Count: ", wk)
    print("Allrounder Count: ", allr)
    print("Bowler Count: ", bowl)
    print("Spinner Count: ", spin)
    print("Pacer Count: ", pace)
    print("Trainee Count: ", trainee)

def ShowcasePlayer(player):
    PrintTitleBoard("Next Player: " + player.name)
    if(player in TopTenAllrounders):
        print("He is one of the top contenders of this years best all rounder award.")

    elif(player in TopTenBatsmen):
        print("He is one of the top contenders of this years best batsmen award.")

    elif(player in TopTenBowlers):
        print("He is one of the top contenders of this years best bowler award.")

    if(player in TopEightWicketkeepers):
        print("He should be a regular in one of the teams for sure.")
    
    if(player in TopTenPacers):
        print("Very few pacers out there with skills like his.")
    elif (player in TopTenSpinners):
        print("Just give him the ball and watch it spin all the way.")

    if (player in TopTenOpeners):
        print("Which team will he open for this year.")
    if(player in TopTenFamous):
        print("He's got a lot of fans around the world.")

    print("He is well known as a", player.position)

    if(player.position == "Batsmen" or player.position == "Wicketkeeper"):
        # Add Traits based commentary here later
        if(player.batting > 90):
            print("Definitely one of the best batsmen I've ever seen playing.")
        elif(player.batting > 80):
            print("He's quite good with his footwork.")
        print("He's got a batting score of:", player.batting)
    
    elif(player.position == "Bowler"):
        # Add Traits based commentary here later
        if(player.bowling > 90):
            print("Definitely one of the best bowlers I've ever witnessed.")
        elif(player.bowling > 80):
            print("He's quite adept with his bowling.")
        print("He's got a bowling score of:", player.bowling)
    
    elif(player.position == "Allrounder"):
        # Add Traits based commentary here later
        if(player.bowling > 90 and player.batting > 90):
            print("Is there anything he's not good at?")
        elif(player.bowling > 80 and player.batting > 80):
            print("Good with the bowl and the bat.")

        print("He's got a batting score of: ", player.batting)
        print("He's got a bowling score of: ", player.bowling)
    
    if player.fielding > 90:
        print("He's also a terrific fielder. Nothing gets past him.")
    elif player.fielding > 80:
        print("His fielding skill is also remarkable")
    
    print(player.estimated_price)
    if(player.estimated_price > 100):
        print("I don't think any team is willing to let him go for a low price: ")
        print("If I had to say a price, I wouldn't suggest anything less than", int(player.estimated_price/10)*10, "Million")
    if(player.estimated_price < 50):
        print("What do you think, will he be bought this time?")
        print("If I had to say a price, I wouldn't suggest anything more than", (int(player.estimated_price/10)+1)*10, "Million")

# printSummaryOfGeneration()
# countRatio(ListOfPlayers)

printSummaryOfGeneration()

print(f'BatsmenAbove80: {len(PlayersAbove80Batting)}')
print(f'BowlersAbove80: {len(PlayersAbove80Bowling)}')
print(f'AllrounderAbove80: {len(PlayersAbove80Allrounder)}')
print(f'PacerAbove80: {len(PlayersAbove80Pace)}')
print(f'SpinnerAbove80: {len(PlayersAbove80Spin)}')


NUM_OF_TEAMS = 13

teamNames = []

for i in range(NUM_OF_TEAMS):
    teamNames.append(createTeamName())
    print(teamNames[i])
    
input()

teamShortList, rivalsForPlayers = makeShortList(list(PlayersAbove80), teamNames)



BidderList = []
TeamList = []

for i in range(NUM_OF_TEAMS):
    TeamList.append(Team(teamNames[i]))

# Rajshahi = Team("Rajshahi")
# Dhaka = Team("Dhaka")
# Sylhet = Team("Sylhet")
# Khulna = Team("Khulna")
# Barishal = Team("Barishal")
# Noakhali = Team("Noakhali")
# Chittagong = Team("Chittagong")
# Rangpur = Team("Rangpur")
# Cumilla = Team("Cumilla")



# def printTeamShortLists():
#     for teamShort in teamShortList:
#         print("###", teamShort, "###")
#         teamShortList[teamShort].printShortList()
#         print("")

# def printPlayerRivals():
#     for player in rivalsForPlayers:
#         print("Teams eyeing him: ", rivalsForPlayers[player])
#         player.printSummary()

# printTeamShortLists()
# printPlayerRivals()


unsold_players = []

RajshahiIdeal = {
    "Batsmen" : 8,
    "Spinner": 3,
    "Pacer": 5,
    "Allrounder": 3,
    "Wicketkeeper": 2,
    "Trainee": 0
}
Possible_Traits = ['Safe', 'Risky', 'Patient', 'Rigid', 'Flexible']
BUDGET = 2000
for i in range(NUM_OF_TEAMS):
    trait = random.choice(Possible_Traits)
    name = teamNames[i]
    BidderList.append(UtilityBasedBidder(
        name,
        trait,
        BUDGET,
        TeamList[i],
        [],
        teamShortList[name],
        []
    ))


print(len(BidderList))
input()
highestPrice = 0
for p in ListOfPlayers:
    ShowcasePlayer(p)
    not_sold = True
    placed_bid_this_round = False
    print("The player is now going up for bidding.")
    #time.sleep(1)
    currentBidder = 0
    bidCounter = 0
    running_price = 10
    run = 0

    if p in rivalsForPlayers.keys() :
        print("Teams eyeing him: ", rivalsForPlayers[p])
    while(not_sold):
        # input()
        print("Reminder to everyone", p.name, "'s current price is", running_price)
        if(bidCounter == 0):
            print("Do I get a bid from anyone?")
            #time.sleep(1)
            run = run + 1
        if(bidCounter == 1):
            print("Going once.")
            #time.sleep(1)
        if(bidCounter == 2):
            print("Going Twice..")
            #time.sleep(1)
        if(bidCounter == 3):
            print("Going Thrice...")
            print("")
            print("#SOLD SOLD SOLD#")
            print(p.name, "sold to", currentBidder.name, "for", running_price, "(", p.estimated_price, ")")
            print("#SOLD SOLD SOLD#")
            print("")
            currentBidder.subtractPrice(running_price)
            not_sold = False
            p.setSellingPrice(running_price)
            currentBidder.addPlayerToTeam(p)
            highestPrice = max(highestPrice, running_price)

            #time.sleep(2)
        if(run > 2):
            print(p.name, "remains unsold.")
            not_sold = False
            unsold_players.append(p)
            #time.sleep(1)
            continue

        placed_bid_this_round = False
        for bidder in BidderList:
            print(bidder.name, bidder.trait, f"-UTILITY: {bidder.playerUtility}")

        # input()
        random.shuffle(BidderList)
        for bidder in BidderList:
            if bidder != currentBidder:
                if bidder.placeBid(p, running_price+5) == 1:
                    if bidCounter == 0:
                        print("We get a bid from", bidder.name)
                    if bidCounter == 1:
                        print("We get another bid from", bidder.name)
                    if bidCounter == 2:
                        print("Another count, and he would have been sold to", currentBidder.name, "but we have a bid from", bidder.name)
                    placed_bid_this_round = True
                    running_price = running_price + random.choice([2, 3, 4, 5])
                    bidCounter = 1
                    currentBidder = bidder
                    
        if(placed_bid_this_round == False and bidCounter != 0):
            bidCounter =  bidCounter +1


print("We will be going once again over the players who are left unsold from the first time.")
input()


for p in unsold_players:
    ShowcasePlayer(p)
    not_sold = True
    placed_bid_this_round = False
    print("The player is now going up for bidding.")
    #time.sleep(1)
    currentBidder = 0
    bidCounter = 0
    running_price = 10
    run = 0

    if p in rivalsForPlayers.keys() :
        print("Teams eyeing him: ", rivalsForPlayers[p])
    while(not_sold):
        print("Reminder to everyone", p.name, "'s current price is", running_price)
        if(bidCounter == 0):
            print("Do I get a bid from anyone?")
            #time.sleep(1)
            run = run + 1
        if(bidCounter == 1):
            print("Going once.")
            #time.sleep(1)
        if(bidCounter == 2):
            print("Going Twice..")
            #time.sleep(1)
        if(bidCounter == 3):
            print("Going Thrice...")
            print("")
            print("#SOLD SOLD SOLD#")
            print(p.name, "sold to", currentBidder.name, "for", running_price, "(", p.estimated_price, ")")
            print("#SOLD SOLD SOLD#")
            print("")
            unsold_players.remove(p)
            currentBidder.subtractPrice(running_price)
            not_sold = False
            p.setSellingPrice(running_price)
            currentBidder.addPlayerToTeam(p)

            #time.sleep(2)
        if(run > 2):
            print(p.name, "remains unsold.")
            not_sold = False
            
            #time.sleep(1)
            continue

        placed_bid_this_round = False
        for bidder in BidderList:
            print(bidder.name, f"-UTILITY: {bidder.playerUtility}")
        # input()
        random.shuffle(BidderList)
        for bidder in BidderList:
            if bidder != currentBidder:
                if bidder.placeBid(p, running_price+5) == 1:
                    if bidCounter == 0:
                        print("We get a bid from", bidder.name)
                    if bidCounter == 1:
                        print("We get another bid from", bidder.name)
                    if bidCounter == 2:
                        print("Another count, and he would have been sold to", currentBidder.name, "but we have a bid from", bidder.name)
                    placed_bid_this_round = True
                    running_price = running_price + 2
                    bidCounter = 1
                    currentBidder = bidder
                    
        if(placed_bid_this_round == False and bidCounter != 0):
            bidCounter =  bidCounter +1

print("HIGHEST PRICE: ", highestPrice)
print()
print()
print()
print()
print("NOW TIME FOR THE TEAMS TO PRESENT THEMSELVES")  

# #time.sleep(2)

TeamLineupRatings = {}

for bd in BidderList:
    
    PrintTitleBoard(bd.name)
    print("Remaining Budget: ", bd.budget)
    # #time.sleep(2)
    # bd.team.printTeamData()
    # printTeamPositionAndOrderSummary(bd.team)
    findTeamStrength(bd.team)
    input()
    # Generate Team Strengths and Weaknesses from the gathered Squad
    # Insert the strength and weakness into the starting eleven creator
    startEleven = StartingEleven()
    
    startEleven.createStartingEleven(bd.team)
    input()
    print()
    print()
    TeamLineupRatings[bd.name] = {"Bidder": bd.trait, "Batting" :startEleven.evaluateBatting() , "Bowling" :startEleven.evaluateBowling(), "Fielding": startEleven.evaluateFielding()}
    startEleven.printBench()
    # #time.sleep(2)
    # print()
    # startEleven.printBenchedPlayers()
# DhakaStart = StartingEleven()
# DhakaStart.createStartingEleven(Dhaka)
# DhakaStart.printBenchedPlayers()
# # Rangpur.printAllPlayerData()

# Rangpur.findBestBatsman().printDetails()
# Rangpur.findBestBowler().printDetails()
# Rangpur.findMostPopular().printDetails()
    
print()
print()
print()
for t in TeamLineupRatings:
    print(f"{t} : {TeamLineupRatings[t]}")


print(len(unsold_players))


k = input()

print("Now for the unsold players")
for pl in unsold_players:
    pl.printInLine()