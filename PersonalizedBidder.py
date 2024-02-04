import random
from ProbabilisticFunctionsModule import get_random_normal_distribution_number_biased

class PersonalizedBidder:
    def __init__(self):
        self.wicket_keeper_budget = 0
        self.batsmen_budget = 0
        self.bowler_budget = 0
        self.spinner_budget = 0
        self.pacer_budget = 0

        self.focus = random.choice(["Pace", "Spin", "Bowling", "Batting", "Balanced"])
        # Likeness to go over estimated price
        self.over_estimate = get_random_normal_distribution_number_biased()

        # Likeness to increase price when price is too low for a player

        self.price_increaser = get_random_normal_distribution_number_biased()

        # Likeness to follow ideal team combination

        self.strictness = get_random_normal_distribution_number_biased()

        # Likeness to fixate on a player

        self.fixation = get_random_normal_distribution_number_biased()

        # Strategic thinking

        self.strategy = get_random_normal_distribution_number_biased()

        # Budget Allocation
        self.budget_handling = get_random_normal_distribution_number_biased()

    
    def initiateBudgets(self, budget):
        variability = 10 - self.strictness
        wk_ct = 2
        batsmen_ct = 7
        bowler_ct = 7
        pace_ct = 4
        spin_ct = 3
        all_rounder_ct = 4
        if(self.focus == "Balanced"):
            wk_ct = 2
            batsmen_ct = 7
            bowler_ct = 7
            all_rounder_ct = 4
        elif(self.focus == "Batting"):
            wk_ct = 2
            batsmen_ct = 8
            bowler_ct = 6
            all_rounder_ct = 4
        elif(self.focus == "Pace"):
            wk_ct = 2
            batsmen_ct = 5
            bowler_ct = 8
            pace_ct = 5
            spin_ct = 3
            all_rounder_ct = 5
        elif(self.focus == "Spin"):
            wk_ct = 2
            batsmen_ct = 5
            bowler_ct = 8
            pace_ct = 4
            spin_ct = 4
            all_rounder_ct = 5
        elif(self.focus == "Bowling"):
            wk_ct = 2
            batsmen_ct = 5
            bowler_ct = 8
            pace_ct = random.choice([4, 5])
            spin_ct = bowler_ct - pace_ct
            all_rounder_ct = 5
        self.wicket_keeper_budget = 0
        self.batsmen_budget = 0
        self.bowler_budget = 0


        self.spinner_budget = 0
        self.pacer_budget = 0
    def placeBid(self, player, running_price):
        pass

    def subtractPrice(self, running_price):
        self.budget = self.budget - running_price
    
    def addPlayerToTeam(self, player):
        self.team.addPlayer(player) 

    def PrintStats(self):
        print("Going over price: ", self.over_estimate)
        print("Increasing rice: ", self.price_increaser)
        print("Fixating on a player: ", self.fixation)
        print("Strategy: ", self.strategy)
        print("Budget Allocation: ", self.budget_handling)