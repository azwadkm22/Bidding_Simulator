import json
from Team.team_strength import find_team_strength
from Team.starting_eleven import StartingEleven
from Team.team import Team
from Player.generate_players import get_list_of_players
from Player.player_generation_stats import PlayerGenStat
from Team.generate_teams import generate_teams, generate_bidders
from Team.team_generation_stats import TeamGenStat
from bidding_simulation import BiddingSimulation
from Utils.showcase_utils import *
from Bidders.user_bidder import UserBidder
# Generate Players
ListOfPlayers = get_list_of_players(100)
ListOfPlayers = sorted(ListOfPlayers, key=lambda Player: Player.estimated_price, reverse=True)

current_player_generation = PlayerGenStat(ListOfPlayers)

# input()
print_summary_of_generation(current_player_generation)

# input()
count_ratio(current_player_generation)


# input()
for p in current_player_generation.players_above_90:
     p.printInLine()
     print()

# input()

# Generate Teams
NUM_OF_TEAMS = 4

team_list = generate_teams(NUM_OF_TEAMS)

current_team_generation = TeamGenStat(team_list=team_list, player_generation=current_player_generation)

bidder_list = generate_bidders(NUM_OF_TEAMS, current_team_generation)

user_team_name = "Azwads Team"
user_team = Team(69, user_team_name)
user_bidder = UserBidder(user_team_name, 20000, user_team)

printTeamShortLists(current_team_generation)
printPlayerRivals(current_team_generation)

# Bidding Simulation

simulation = BiddingSimulation(user_bidder, bidder_list=bidder_list, player_generation=current_player_generation, team_generation=current_team_generation)

simulation.simulate_bidding(sleep_time=0)

print("We will be going once again over the players who are left unsold from the first time.")
input()

simulation.simulate_bidding(sleep_time=0)

# After effects

print("HIGHEST PRICE: ", simulation.highest_price)
print("NOW TIME FOR THE TEAMS TO PRESENT THEMSELVES")  

team_lineup_ratings = {}
team_data = {}
team_lineups = {}

for bd in bidder_list:
    input()
    lineup_data = {}
    print_title_board(bd.name)
    print(bd.trait)
    print("Remaining Budget: ", bd.budget)
    find_team_strength(bd.team)

    team_data[bd.team.name] = bd.team.get_team_data_to_JSON()

    input()
    # TODO:Generate Team Strengths and Weaknesses from the gathered Squad
    # TODO:Insert the strength and weakness into the starting eleven creator

    startEleven = StartingEleven()
    
    starting_eleven = startEleven.create_starting_eleven(bd.team)
    lineup = {}
    for i in range(len(starting_eleven)):
        lineup[i] = starting_eleven[i].player_id

    lineup_data["starting_lineup"] = lineup
    lineup_data["batting"] = startEleven.evaluate_batting() 
    lineup_data["bowling"] = startEleven.evaluate_bowling()
    lineup_data["fielding"] = startEleven.evaluate_fielding()
    lineup_data["bench"] = startEleven.print_bench()

    team_lineups[bd.team.name] = lineup_data   

    print(lineup_data) 

print_title_board(user_bidder.name)

team_data[user_bidder.name] = user_bidder.team.get_team_data_to_JSON()

startEleven = StartingEleven()

starting_eleven = startEleven.create_starting_eleven(user_bidder.team)
lineup = {}
for i in range(len(starting_eleven)):
    lineup[i] = starting_eleven[i].player_id

lineup_data["starting_lineup"] = lineup
lineup_data["batting"] = startEleven.evaluate_batting() 
lineup_data["bowling"] = startEleven.evaluate_bowling()
lineup_data["fielding"] = startEleven.evaluate_fielding()
lineup_data["bench"] = startEleven.print_bench()
team_lineups[bd.team.name] = lineup_data 

with open(f"./generated/team_data.json", 'w') as f:
        json.dump(team_data, f, indent=4)

with open(f"./generated/team_lineups.json", 'w') as f:
        json.dump(team_lineups, f, indent=4)
    
print()
for t in team_lineup_ratings:
    print(f"{t} : {team_lineup_ratings[t]}")

print(len(simulation.list_of_unsold_players))

k = input()

print("Now for the unsold players")
for pl in simulation.list_of_unsold_players:
    pl.printInLine()