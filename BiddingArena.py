from PlayerGenerator import Player
from TeamGenerator import Team
from Bidders import RandomBidder, AlwaysBidder, NeverBidder

def GenerateNPlayerList(n):
    ListOfPlayers = []

    for i in range(n):
        NewPlayer = Player()
        ListOfPlayers.append(NewPlayer)
    return ListOfPlayers


def FindTopNPlayerInCategory(playerList, n, category):
    if(category == "Fame"):
        playerList = sorted(playerList, key=lambda Player: Player.fame, reverse=True)
        TopNPlayers = playerList[:n]
        return TopNPlayers

    if(category == "Batting"):
        playerList = sorted(playerList, key=lambda Player: Player.batting, reverse=True)
        TopNPlayers = playerList[:n]
        return TopNPlayers
    
    if(category == "Bowling"):
        playerList = sorted(playerList, key=lambda Player: Player.bowling, reverse=True)
        TopNPlayers = playerList[:n]
        return TopNPlayers
    
    if(category == "Price"):
        playerList = sorted(playerList, key=lambda Player: Player.estimated_price, reverse=True)
        TopNPlayers = playerList[:n]
        return TopNPlayers

ListOfPlayers = GenerateNPlayerList(10)

TopTenBatsmen = FindTopNPlayerInCategory(ListOfPlayers, 10, "Batting")
TopTenBowler = FindTopNPlayerInCategory(ListOfPlayers, 10, "Bowling")
TopTenFamous = FindTopNPlayerInCategory(ListOfPlayers, 10, "Fame")
TopTenMostExpensive = FindTopNPlayerInCategory(ListOfPlayers, 10, "Price")


def PrintTitleBoard(Title):
    print("########")
    print("")
    print(Title)
    print("")
    print("########")

# PrintTitleBoard("Best Batsmen")
# for pl in TopTenBatsmen:
#     pl.printDetails()
# PrintTitleBoard("Best Bowlers")
# for pl in TopTenBowler:
#     pl.printDetails()
# PrintTitleBoard("Most Famous")
# for pl in TopTenFamous:
#     pl.printDetails()
# PrintTitleBoard("Most Expensive")
# for pl in TopTenMostExpensive:
#     pl.printDetails()


def ShowcasePlayer(player):
    PrintTitleBoard("Next Player: " + player.name)
    if(player in TopTenBatsmen and player in TopTenBowler):
        print("He is one of the top contenders of this years best allrounder award.")

    elif(player in TopTenBatsmen):
        print("He is one of the top contenders of this years best batsmen award.")
    

    elif(player in TopTenBatsmen and player in TopTenBowler):
        print("He is one of the top contenders of this years best bowler award.")

    if(player in TopTenFamous):
        print("He's got a lot of fans around the world.")

    print("He is well known as a", player.position)

    if(player.position == "Batsmen" or player.position == "Wicketkeeper"):
        # Add Traits based commentary here later
        if(player.batting > 90):
            print("Definitely one of the best batsmen I've ever seen playing.")
        elif(player.bowling > 80):
            print("He's quite good with his footwork.")
        print("He's got a batting score of:", player.batting)
    elif(player.position == "Bowler"):
        # Add Traits based commentary here later

        if(player.bowling > 90):
            print("Definitely one of the best bowlers I've ever witnessed.")
        elif(player.bowling > 80):
            print("He's quite good with his bowling.")
        print("He's got a bowling score of:", player.bowling)
    elif(player.position == "Allrounder"):
        # Add Traits based commentary here later
        if(player.bowling > 90 and player.batting > 90):
            print("Is there anything he's not good at?")
        elif(player.bowling > 80 and player.batting > 80):
            print("Good with the bowl and the bat.")

        print("He's got a batting score of: ", player.batting)
        print("He's got a bowling score of: ", player.bowling)
    
    print(player.estimated_price)
    if(player.estimated_price > 75):
        print("I don't think any team is willing to let him go for a low price: ")
        print("If I had to say a price, I wouldn't suggest anything less than", int(player.estimated_price/10)*10, "Million")
    if(player.estimated_price < 40):
        print("What do you think, will he be bought this round?")
        print("If I had to say a price, I wouldn't suggest anything more than", (int(player.estimated_price/10)+1)*10, "Million")



BidderList = []
BidderList.append(RandomBidder("Rajshahi"))
BidderList.append(RandomBidder("Dhaka"))
BidderList.append(RandomBidder("Sylhet"))
BidderList.append(RandomBidder("Khulnda"))
BidderList.append(RandomBidder("Barishal"))
BidderList.append(RandomBidder("Noakhali"))
BidderList.append(RandomBidder("Chittagong"))
BidderList.append(RandomBidder("Rangpur"))


for p in ListOfPlayers:
    ShowcasePlayer(p)
    not_sold = True
    placed_bid_this_round = False
    print("The player is now going up for bidding.")
    currentBidder = 0
    bidCounter = 0
    running_price = 10
    while(not_sold):
        print("Reminder to everyone", p.name, "'s current price is", running_price)
        if(bidCounter == 0):
            print("Do I get a bid from anyone?")
        if(bidCounter == 1):
            print("Going once.")
        if(bidCounter == 2):
            print("Going Twice.")
        if(bidCounter == 3):
            print("Going Thrice.")
            print(p.name, "sold to", currentBidder.name, "for", running_price)
            not_sold = False
        
        placed_bid_this_round = False
        for bidder in BidderList:
            if bidder != currentBidder:
                if bidder.placeBid() == 1:
                    if bidCounter == 0:
                        print("We get a bid from", bidder.name)
                    if bidCounter == 1:
                        print("We get another bid from", bidder.name)
                    if bidCounter == 2:
                        print("Another count, and he would have been sold to", currentBidder.name, "but we have a bid from", bidder.name)
                    placed_bid_this_round = True
                    running_price = running_price + 5
                    bidCounter = 1
                    currentBidder = bidder
                    break
        if(placed_bid_this_round == False and bidCounter != 0):
            bidCounter =  bidCounter +1
        
            
        
        
        