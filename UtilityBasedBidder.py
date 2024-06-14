# Placing a bid for a player depends on
# The players position
# The players skill
# The players current price
# The players estimated price


# The teams current squad
# The teams current position stat of the player
# the teams first 11
# The teams focus

from ProbabilisticFunctionsModule import getProbabilisticAnswer

PlayerDistribution = {
    "Batsmen": 7,
    "Bowler": 7,
    "Allrounder": 5,
    "Wicketkeeper": 2, 
    "Trainee": 0
}

# Utility will be a function of players position
class UtilityBasedBidder:

    def __init__(self, name, trait, budget, team, focus, shortlist, expected_distribution):
        self.focus = focus
        self.trait = trait
        self.budget = budget
        self.team = team
        self.utility = 0
        self.name = name
        self.shortlist = shortlist
        self.playerUtility = 0
        self.expected_distribution = expected_distribution


    def calculateUtility(self, player, running_price):
        utility = 0
        similar_players = self.team.findSimilarTeamPlayers(player)
        
        # print(player.name)
        if similar_players:
            if player.position == "Batsmen":
                utility = utility + (PlayerDistribution[player.position] - len(similar_players))
        else:
            utility = utility + 10

        

        if player.position != "Bowler":
            if player.batting_order == "Opener":
                if len(self.team.getTeamOpeners()) > 3:
                    utility = utility - 10    
            if player.batting_order == "Top Order":  
                if len(self.team.getTeamTopOrder()) > 4:
                    utility = utility - 10          
            if player.batting_order == "Middle Order":
                if len(self.team.getTeamMidOrder()) > 4:
                    utility = utility - 10
            if player.batting_order == "Low Order":
                if len(self.team.getTeamLowOrder()) > 3:
                    utility = utility - 10

        sim_count_ut = utility
        utility = 0


            
        # print("Similar Player Count Utility: ", utility)  
        

        #Increase utility if player is better than similar players
        #Increase utility based on how good the player is compared to team players
        if similar_players:
            for team_player in similar_players:
                if player.position == "Batsmen":
                    if player.batting - team_player.batting > 25:
                        utility = utility + 3
                    elif player.batting - team_player.batting > 15:
                        utility = utility + 2
                    elif player.batting - team_player.batting > 8:
                        utility = utility + 1
                    elif abs(player.batting - team_player.batting) < 5:
                        utility = utility
                    else:
                        utility = utility - 1


                elif player.position == "Wicketkeeper":
                    if player.batting - team_player.batting > 25:
                        utility = utility + 3
                    elif player.batting - team_player.batting > 16:
                        utility = utility + 2
                    elif player.batting - team_player.batting > 8:
                        utility = utility + 1
                    else:
                        utility = utility - 3


                elif player.position == "Bowler":
                    if player.bowling - team_player.bowling > 25:
                        utility = utility + 3
                    elif player.bowling - team_player.bowling > 15:
                        utility = utility + 2
                    elif player.bowling - team_player.bowling > 8:
                        utility = utility + 1
                    elif abs(player.bowling - team_player.bowling) < 5:
                        utility = utility
                    else:
                        utility = utility -1

                elif player.position == "Allrounder":
                    if player.bowling - team_player.bowling > 25:
                        utility = utility + 3
                    elif player.bowling - team_player.bowling > 15:
                        utility = utility + 2
                    elif player.bowling - team_player.bowling > 8:
                        utility = utility + 1
                    elif abs(player.bowling - team_player.bowling) < 5:
                        utility = utility
                    else:
                        utility = utility - 1
                    
                    if player.batting - team_player.batting > 25:
                        utility = utility + 3
                    elif player.batting - team_player.batting > 15:
                        utility = utility + 2
                    elif player.batting - team_player.batting > 8:
                        utility = utility + 1
                    elif abs(player.bowling - team_player.bowling) < 5:
                        utility = utility
                    else:
                        utility = utility -1


        # print("Similar Player Skill Utility: ", utility)  
        player_comp_ut = utility
        utility = 0

        if (player.position == "Batsmen" or player.position == "Wicketkeeper" ):
            if player.batting < 50:
                utility = utility - 5
            elif player.batting < 60:
                utility = utility - 3
            elif player.batting < 70:
                utility = utility - 1
            elif player.batting >= 95:
                utility = utility + 10
            elif player.batting >= 90:
                utility = utility + 8
            elif player.batting >= 85:
                utility = utility + 5
            elif player.batting >= 80:
                utility = utility + 3
            elif player.batting >= 70:
                utility = utility + 1
            

        if (player.position == "Bowler"):
            if player.bowling < 50:
                utility = utility - 5
            elif player.bowling < 60:
                utility = utility - 3
            elif player.bowling < 70:
                utility = utility - 1
            elif player.bowling >= 95:
                utility = utility + 10
            elif player.bowling >= 90:
                utility = utility + 8
            elif player.bowling >= 85:
                utility = utility + 5
            elif player.bowling >= 80:
                utility = utility + 3
            elif player.bowling >= 70:
                utility = utility + 1
        
        if (player.position == "Allrounder"):
            if player.bowling < 50 and player.batting < 50:
                utility = utility - 5
            elif player.bowling < 60 and player.batting < 60:
                utility = utility - 3
            elif player.bowling < 70 and player.batting < 70:
                utility = utility - 1
            elif player.bowling >= 90 and player.batting >= 90:
                utility = utility + 10
            elif player.bowling >= 90 or player.batting >= 90:
                utility = utility + 8
            elif player.bowling >= 80 and player.batting >= 80:
                utility = utility + 5
            elif player.bowling >= 80 or player.batting >= 80:
                utility = utility + 3
            elif player.bowling >= 70 or player.batting >= 70:
                utility = utility + 1

        # print("Player Skill Utility: ", utility)  
        skill_ut = utility
        utility = 0
        #player price utility depends on the running price, player's estimated price, teams remaining budget
        
        if self.budget < running_price:
            utility = -100
        
        # print(player.estimated_price)
        if running_price > 2*player.estimated_price:
            utility = utility - 20
        elif running_price > 1.5*player.estimated_price:
            utility = utility - 15
        elif running_price > 1.4*player.estimated_price:
            utility = utility - 10
        elif running_price > 1.3*player.estimated_price:
            utility = utility - 8
        elif running_price > 1.2*player.estimated_price:
            utility = utility - 5
        elif running_price > 1.1*player.estimated_price:
            utility = utility - 3
        elif running_price > player.estimated_price:
            utility = utility - 1
        
        budget_ut = utility
        # print("Player Price Utility: ", utility)  

        utility = 0
        # print(self.shortlist)
        if player in self.shortlist.players:
            utility = utility + 5
        
        shortlist_ut = utility

        #Remaining budget utility


        #
        average_remaining = self.budget / (21 - self.team.number_of_players)
        if running_price < average_remaining:
            utility = utility + 5
        else:
            utility = utility - 5

        remaining_ut = utility

        utility = 0

        #Player slot left utility
        if self.team.number_of_players < 10:
            utility = utility + 5
        elif self.team.number_of_players < 15:
            utility = utility + 1
        elif self.team.number_of_players > 21:
            utility = utility - 100
        elif self.team.number_of_players > 15:
            utility = utility - 3

        slot_left_ut = utility

        max_possible_utility = 10 + 3 +  PlayerDistribution[player.position] + 20 + 10 + 5 + 10
        if similar_players:
            max_possible_utility = max_possible_utility + len(similar_players)*3
        
        
        total_utility = player_comp_ut + sim_count_ut + skill_ut + budget_ut + shortlist_ut + remaining_ut + slot_left_ut
        
        # print("Total Utility: ", total_utility)
        # print("Max Utility: ", max_possible_utility)
        self.playerUtility = total_utility/max_possible_utility
        return total_utility/max_possible_utility
    

    def placeBid(self, player, running_price):
        
        if self.team.number_of_players > 20:
            return 0
        utility = self.calculateUtility(player, running_price)
        if utility < 0:
            return 0
        elif utility > 1:
            return 1
        else:
            return getProbabilisticAnswer(utility)
    
    def subtractPrice(self, running_price):
        self.budget = self.budget - running_price
    
    def addPlayerToTeam(self, player):
        self.team.addPlayer(player)

