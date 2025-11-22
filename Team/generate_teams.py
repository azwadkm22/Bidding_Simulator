from Team.team import Team
from Team.team_name_generator import createTeamName
from Team.team_generation_stats import TeamGenStat
from Bidders.utility_based_bidder import UtilityBasedBidder
import random

def generate_teams(n):
    team_list = []
    for i in range(n):
        team_list.append(Team(i, createTeamName()))
    return team_list
    

def generate_bidders(n, team_gen_stat : TeamGenStat, budget = 2000):
    bidder_list = []
    possible_traits = ['Safe', 'Risky', 'Patient', 'Rigid', 'Flexible']
    for i in range(n):
        bidder_trait = random.choice(possible_traits)
        name = team_gen_stat.team_list[i].name
        bidder_list.append(UtilityBasedBidder(
            name,
            bidder_trait,
            budget,
            team_gen_stat.team_list[i],
            [],
            team_gen_stat.team_short_list[name],
            []
        ))

    return bidder_list
