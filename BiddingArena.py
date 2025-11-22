import time
import random
import json
from Team.team_strength import findTeamStrength
from Player.player import Player
from Team.team import Team, printTeamPositionAndOrderDetails, printTeamPositionAndOrderSummary
from Team.starting_eleven import StartingEleven
from Team.shortlister import ShortList, makeShortList
from Bidders.utility_based_bidder import UtilityBasedBidder
from Player.generate_players import get_list_of_players
from Player.player_generation_stats import PlayerGenStat

from Team.generate_teams import generate_teams, generate_bidders
from Team.team_generation_stats import TeamGenStat
from Utils.showcase_utils import *

# Generate Players
ListOfPlayers = get_list_of_players(250)
ListOfPlayers = sorted(ListOfPlayers, key=lambda Player: Player.estimated_price, reverse=True)

current_player_generation = PlayerGenStat(ListOfPlayers)
print_summary_of_generation(current_player_generation)
count_ratio(current_player_generation)

# Generate Teams
NUM_OF_TEAMS = 13

team_list = generate_teams(NUM_OF_TEAMS)

current_team_generation = TeamGenStat(team_list=team_list, player_generation=current_player_generation)

bidder_list = generate_bidders(NUM_OF_TEAMS, current_team_generation)

printTeamShortLists(current_team_generation)
printPlayerRivals(current_team_generation)

unsold_players = []
highestPrice = 0
for p in ListOfPlayers:
    showcase_player(p, current_player_generation)
    not_sold = True
    placed_bid_this_round = False
    print("The player is now going up for bidding.")
    ##time.sleep(1)
    currentBidder = 0
    bidCounter = 0
    running_price = 10
    run = 0

    if p in current_team_generation.rivals_for_players.keys() :
        print("Teams eyeing him: ", current_team_generation.rivals_for_players[p])
    while(not_sold):
        # input()
        print("Reminder to everyone", p.name, "'s current price is", running_price)
        if(bidCounter == 0):
            print("Do I get a bid from anyone?")
            ##time.sleep(1)
            run = run + 1
        if(bidCounter == 1):
            print("Going once.")
            ##time.sleep(1)
        if(bidCounter == 2):
            print("Going Twice..")
            ##time.sleep(1)
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

            ##time.sleep(2)
        if(run > 2):
            print(p.name, "remains unsold.")
            not_sold = False
            unsold_players.append(p)
            ##time.sleep(1)
            continue

        placed_bid_this_round = False
        for bidder in bidder_list:
            print(bidder.name, bidder.trait, f"-UTILITY: {bidder.playerUtility}")

        # input()
        random.shuffle(bidder_list)
        for bidder in bidder_list:
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
    showcase_player(p, current_player_generation)
    not_sold = True
    placed_bid_this_round = False
    print("The player is now going up for bidding.")
    #time.sleep(1)
    currentBidder = 0
    bidCounter = 0
    running_price = 10
    run = 0

    if p in current_team_generation.rivals_for_players.keys() :
        print("Teams eyeing him: ", current_team_generation.rivals_for_players[p])
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
            
            ##time.sleep(1)
            continue

        placed_bid_this_round = False
        for bidder in bidder_list:
            print(bidder.name, f"-UTILITY: {bidder.playerUtility}")
        # input()
        random.shuffle(bidder_list)
        for bidder in bidder_list:
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

# ##time.sleep(2)

TeamLineupRatings = {}

for bd in bidder_list:
    
    print_title_board(bd.name)
    print("Remaining Budget: ", bd.budget)
    # ##time.sleep(2)
    # bd.team.printTeamData()
    # printTeamPositionAndOrderSummary(bd.team)
    findTeamStrength(bd.team)
    team_json_data = bd.team.get_team_data_to_JSON()


    with open(f"./generated/teams/{bd.name}.json", 'w') as f:
        json.dump(team_json_data, f, indent=4)

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
    # ##time.sleep(2)
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