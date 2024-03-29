import time
from PlayerGenerator import Player
from TeamGenerator import Team, printTeamPositionAndOrderDetails, printTeamPositionAndOrderSummary
from Bidders import RandomBidder, AlwaysBidder, NeverBidder, SafeBidder, RiskyBidder, PriorityBidder, SpecializedBidder, SpecialBidder
from StartingEleven import StartingEleven
from Shortlister import ShortList, makeShortList

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

TopTenBatsmen = FindTopNPlayerInCategory(ListOfPlayers, 10, "Batting")
TopTenBowlers = FindTopNPlayerInCategory(ListOfPlayers, 10, "Bowling")
TopTenSpinners = FindTopNPlayerInCategory(ListOfPlayers, 10, "Spinner")
TopTenPacers = FindTopNPlayerInCategory(ListOfPlayers, 10, "Pacer")
TopEightWicketkeepers = FindTopNPlayerInCategory(ListOfPlayers, 24, "Wicketkeeper")
TopTenOpeners = FindTopNPlayerInCategory(ListOfPlayers, 10, "Opener")
TopTenAllrounders = FindTopNPlayerInCategory(ListOfPlayers, 10, "Allrounder")
TopTenFamous = FindTopNPlayerInCategory(ListOfPlayers, 10, "Fame")
TopTenMostExpensive = FindTopNPlayerInCategory(ListOfPlayers, 10, "Price")




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
            player.printSummary()

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
BidderList = []
TeamList = []

Rajshahi = Team("Rajshahi")
Dhaka = Team("Dhaka")
Sylhet = Team("Sylhet")
Khulna = Team("Khulna")
Barishal = Team("Barishal")
Noakhali = Team("Noakhali")
Chittagong = Team("Chittagong")
Rangpur = Team("Rangpur")
Cumilla = Team("Cumilla")

# Dhaka, Rajshahi, Rangpur, Barishal, Chittagong, Cumilla, Sylhet, Khulna

# BidderList.append(SpecializedBidder("Rajshahi", 5000, Rajshahi, "Batting"))
# BidderList.append(PriorityBidder("Dhaka", 5000, Dhaka))
# BidderList.append(PriorityBidder("Sylhet", 5000, Sylhet))
# BidderList.append(PriorityBidder("Khulna", 5000, Khulna))
# BidderList.append(PriorityBidder("Barishal", 5000, Barishal))
# BidderList.append(PriorityBidder("Noakhali", 5000, Noakhali))
# BidderList.append(PriorityBidder("Chittagong", 5000, Chittagong))
# # BidderList.append(PriorityBidder("Rangpur", 5000, Rangpur))

# BidderList.append(SpecializedBidder("Rangpur", 5000, Rangpur, "Batting"))

BidderList.append(SpecialBidder("RAJ", 5000, Rajshahi, []))
BidderList.append(SpecialBidder("RAN", 5000, Rangpur, []))
BidderList.append(SpecialBidder("DHK", 10000, Dhaka, []))
BidderList.append(SpecialBidder("SYL", 5000, Sylhet, []))
BidderList.append(SpecialBidder("BAR", 5000, Barishal, []))
BidderList.append(SpecialBidder("KHU", 5000, Khulna, []))
BidderList.append(SpecialBidder("CTG", 5000, Chittagong, []))
BidderList.append(SpecialBidder("COM", 5000, Cumilla, []))
BidderList.append(SpecialBidder("NKH", 5000, Noakhali, []))



teamNames = [
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
    "Rangpur"
]

teamShortList, rivalsForPlayers = makeShortList(list(PlayersAbove80), teamNames)

def printTeamShortLists():
    for teamShort in teamShortList:
        print("###", teamShort, "###")
        teamShortList[teamShort].printShortList()
        print("")

def printPlayerRivals():
    for player in rivalsForPlayers:
        print("Teams eyeing him: ", rivalsForPlayers[player])
        player.printSummary()

printTeamShortLists()
printPlayerRivals()
# for p in ListOfPlayers:
#     ShowcasePlayer(p)
#     not_sold = True
#     placed_bid_this_round = False
#     print("The player is now going up for bidding.")
#     # time.sleep(2)
#     currentBidder = 0
#     bidCounter = 0
#     running_price = 10  
#     run = 0
#     while(not_sold):
#         print("Reminder to everyone", p.name, "'s current price is", running_price)
#         if(bidCounter == 0):
#             print("Do I get a bid from anyone?")
#             # time.sleep(1)
#             run = run + 1
#         if(bidCounter == 1):
#             print("Going once.")
#             # time.sleep(1)
#         if(bidCounter == 2):
#             print("Going Twice..")
#             # time.sleep(1)
#         if(bidCounter == 3):
#             print("Going Thrice...")
#             # time.sleep(1)
#             print(p.name, "sold to", currentBidder.name, "for", running_price)
#             currentBidder.subtractPrice(running_price)
#             not_sold = False
#             p.setSellingPrice(running_price)
#             currentBidder.addPlayerToTeam(p)
#         if(run > 2):
#             print(p.name, "remains unsold.")
#             not_sold = False
#             continue

        
#         placed_bid_this_round = False
#         for bidder in BidderList:
#             if bidder != currentBidder:
#                 if bidder.placeBid(p, running_price+5) == 1:
#                     if bidCounter == 0:
#                         print("We get a bid from", bidder.name)
#                     if bidCounter == 1:
#                         print("We get another bid from", bidder.name)
#                     if bidCounter == 2:
#                         print("Another count, and he would have been sold to", currentBidder.name, "but we have a bid from", bidder.name)
#                     placed_bid_this_round = True
#                     running_price = running_price + 5
#                     bidCounter = 1
#                     currentBidder = bidder
                    
#         if(placed_bid_this_round == False and bidCounter != 0):
#             bidCounter =  bidCounter +1
        
            
        
# for bd in BidderList:
#     PrintTitleBoard(bd.name)
#     print("Remaining Budget: ", bd.budget)
#     bd.team.printTeamData()
    # printTeamPositionAndOrderSummary(bd.team)
    
# DhakaStart = StartingEleven()
# DhakaStart.createStartingEleven(Dhaka)
# DhakaStart.printBenchedPlayers()
# # Rangpur.printAllPlayerData()

# Rangpur.findBestBatsman().printDetails()
# Rangpur.findBestBowler().printDetails()
# Rangpur.findMostPopular().printDetails()

