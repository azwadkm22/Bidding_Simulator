import json
from Team.team_strength import findTeamStrength
from Team.starting_eleven import StartingEleven
from Player.generate_players import get_list_of_players
from Player.player_generation_stats import PlayerGenStat
from Team.generate_teams import generate_teams, generate_bidders
from Team.team_generation_stats import TeamGenStat
from bidding_simulation import BiddingSimulation
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

# Bidding Simulation

simulation = BiddingSimulation(bidder_list=bidder_list, player_generation=current_player_generation, team_generation=current_team_generation)

simulation.simulate_bidding()

print("We will be going once again over the players who are left unsold from the first time.")
input()

simulation.simulate_bidding()

# After effects

print("HIGHEST PRICE: ", simulation.highest_price)
print("NOW TIME FOR THE TEAMS TO PRESENT THEMSELVES")  

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


print(len(simulation.list_of_unsold_players))


k = input()

print("Now for the unsold players")
for pl in simulation.list_of_unsold_players:
    pl.printInLine()