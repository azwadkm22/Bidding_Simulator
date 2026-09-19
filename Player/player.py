
from Player.name_generator.player_name_generator import getDomesticPlayerName, getInternationalPlayerName

from random import randint
from Utils.probability_utils import get_random_normal_distribution_number_biased
import random

class Player():
    # Overridden by DomesticPlayer/InternationalPlayer before they call
    # super().__init__() - these class-level defaults only apply if Player is
    # ever instantiated directly (e.g. reconstructing from json_data saved
    # before this field existed), so get_JSON_data() never crashes.
    nationality = "Domestic"
    player_type = "Domestic"

    def __init__(self, player_id, json_data = None):
        if json_data == None:
            self.player_id = player_id
            # No default name here on purpose - a fresh (no json_data) Player
            # must come from DomesticPlayer/InternationalPlayer, which set
            # self.name before calling super().__init__(). A plain Player()
            # with no json_data and no name is a bug, not a case to paper
            # over with a placeholder.
            self.batting = get_random_normal_distribution_number_biased(25, 94)
            bowlSkillStart = 20
            if self.batting >= 70:
                bowlSkillStart = 15
            elif self.batting <= 50:
                bowlSkillStart = 35
            self.bowling = get_random_normal_distribution_number_biased(bowlSkillStart, 94)
            self.fielding = get_random_normal_distribution_number_biased(
                max(self.batting, self.bowling) - 30, min(max(self.batting, self.bowling) + 20, 90))
            self.position = self.getPosition()
            if self.position == "Trainee":
                self.fielding = 50
            self.fame = 50 #get_random_normal_distribution_number_biased
            self.estimated_price = self.getEstimatedPrice()
            self.batting_hand = random.choice(["Left", "Right"])
            self.bowling_type = random.choice(["Spinner", "Pacer"])
            self.bowling_style = self.pickBowlingStyle()
            self.batting_order = self.pickBattingOrder()
            
            self.selling_price = 0
        else:
            self.player_id = player_id
            self.name = json_data["name"]
            self.batting = json_data["batting"]
            self.bowling = json_data["bowling"]
            self.fielding = json_data["fielding"]
            self.position = json_data["position"]
            self.fame = json_data["fame"]
            self.estimated_price = json_data["estimated_price"]
            self.batting_hand = json_data["batting_hand"]
            self.bowling_type = json_data["bowling_type"]
            self.bowling_style = json_data["bowling_style"]
            self.batting_order = json_data["batting_order"]
            self.selling_price = json_data["selling_price"]
 
    def printDetails(self):
        print(self.name)
        print("Batting Skill: ", self.batting)
        print("Bowling Skill: ", self.bowling)
        print("Fielding Skill: ", self.fielding)
        print("Position: ", self.position)
        print("Fame: ", self.fame)
        print("Estimated Price: ", self.estimated_price)
        print("Batting Hand: ", self.batting_hand)
        print("Batting Order: ", self.batting_order)
        print("Bowling Type: ", self.bowling_type)
        print("Bowling Style: ", self.bowling_style)
        print("")

    def setSellingPrice(self, price):
        self.selling_price = price

    def printSkill(self):
        print(self.name)
        print("Batting Skill: ", self.batting)
        print("Bowling Skill: ", self.bowling)
        print("Fielding Skill: ", self.fielding)
        print("")

    def printSummary(self):
        print(self.name)
        print("Position: ", self.position)
        if(self.position == "Batsmen"):
            print("Batting Skill: ", self.batting)
        elif (self.position == "Wicketkeeper"):
            print("Batting Skill: ", self.batting)
            print("Fielding Skill: ", self.fielding)
        elif(self.position == "Bowler"):
            print("Bowling Skill: ", self.bowling)
            print("Bowling Type: ", self.bowling_type)
        else:
            print("Batting Skill: ", self.batting)
            print("Bowling Skill: ", self.bowling)
            print("Bowling Type: ", self.bowling_type)        
        print("Batting Order: ", self.batting_order)
        print("")

    def printPosition(self):
        print(self.name)
        print("Position: ", self.position)
        print("Estimated Price: ", self.estimated_price)

    def printName(self):
        print(self.name)

    def printInLine(self):
        print(f'{self.name}: ', end="")
        if self.position == "Batsmen":
            print(f'BAT({self.batting}) {self.batting_order} Batsmen', end="")
        if self.position == "Wicketkeeper":
            print(f'BAT({self.batting}) Wicketkeeper', end="")
        if self.position == "Bowler":
            if self.bowling_type == "Pacer":
                print(f'BWL({self.bowling}) Pacer', end="")
            else:
                print(f'BWL({self.bowling}) Spinner', end="")
        if self.position == "Allrounder":
            if self.bowling_type == "Pacer":
                print(f'BAT({self.batting}) BWL({self.bowling}) Allrounder Pacer', end="")
            else:
                print(f'BAT({self.batting}) BWL({self.bowling}) Allrounder Spinner', end="")

        if self.selling_price != 0:
            print(f' Sold At:{self.selling_price}', end="")

        print(f', Est: {self.estimated_price}')

    def getPosition(self):
        if self.batting < 60 and self.bowling < 60:
            return "Trainee"
        
        if((abs(self.batting - self.bowling) < 10 and self.batting > 60) or (self.batting > 75 and self.bowling > 70)):
            return "Allrounder"
        elif(self.batting > self.bowling):
            if(self.bowling < 40 and self.fielding > 75):
                return "Wicketkeeper"
            elif (self.batting - self.bowling > 30 and self.fielding > 70 and self.batting > 80):
                return "Wicketkeeper"
            else:
                return "Batsmen"
        elif self.bowling > self.batting:
            return "Bowler"
        else:
            return "Trainee"
        
    def pickBowlingStyle(self):
        if self.bowling_type == "Spinner":
            return random.choice(["Off-Spin", "Leg-Spin", "Left-arm orthodox spin", "Left-arm unorthodox spin"])
        else:
            if(self.bowling > 95):
                return "Fast"
            elif(self.bowling > 90):
                return random.choice(["Fast", "Fast-medium"])
            elif(self.bowling > 80):
                return random.choice(["Fast", "Fast-medium", "Medium"])
            elif(self.bowling > 70):
                return random.choice(["Fast-medium", "Medium", "Slow"])
            else:
                return random.choice(["Medium", "Slow"])

    def pickBattingOrder(self):
        if self.position == "Bowler":
            return "Low Order"
        
        roll = random.randint(0, 100)
        if(roll > 75):
            return "Opener"
        elif(roll > 45):
            return "Top Order"
        elif(roll > 15):
            return "Middle Order"
        else:
            return "Low Order"

    def getEstimatedPrice(self):
        # Position-weighted skill rating on a 0-100 scale (weights mirror the
        # old formula's ratios), then a quadratic curve so genuine stars cost
        # disproportionately more than merely-good players, instead of a
        # near-linear spread - closer to how real auctions price a handful of
        # marquee names far above the rest of the field.
        rating = 0.0
        rating = max(rating, 0.9 * self.batting + 0.1 * self.fielding)
        rating = max(rating, 0.9 * self.bowling + 0.1 * self.fielding)
        rating = max(rating, 0.85 * self.batting + 0.15 * self.fielding)
        rating = max(rating, 0.45 * self.batting + 0.45 * self.bowling + 0.1 * self.fielding)

        peak_skill = max(self.batting, self.bowling)
        price_multiplier = 0.2 + (peak_skill / 99) ** 3
        # price_multiplier = 1

        price = round(0.022 * rating ** 2 * price_multiplier)

        return max(price, 10)
    
    def get_JSON_data(self):
        return {
            "name": self.name,
            "batting": self.batting,
            "bowling": self.bowling,
            "fielding": self.fielding,
            "position": self.position,
            "fame": self.fame,
            "estimated_price": self.estimated_price,
            "batting_hand": self.batting_hand,
            "bowling_type": self.bowling_type,
            "bowling_style": self.bowling_style,
            "batting_order": self.batting_order,
            "selling_price": self.selling_price,
            "nationality": self.nationality,
            "player_type": self.player_type,
        }

class DomesticPlayer(Player):
    def __init__(self, player_id, json_data = None):
        self.name = getDomesticPlayerName()
        self.nationality = "Bangladeshi"
        self.player_type = "Domestic"
        super().__init__(player_id, json_data)


class InternationalPlayer(Player):
    def __init__(self, player_id, json_data = None):
        self.name = getInternationalPlayerName()
        # Placeholder - real per-country nationalities come later; player_type
        # is the stable field to filter/branch on, since nationality here is
        # expected to change shape as this gets expanded.
        self.nationality = "International"
        self.player_type = "International"
        super().__init__(player_id, json_data)


PLAYER_TYPE_CLASSES = {"Domestic": DomesticPlayer, "International": InternationalPlayer}


def build_player(player_id, json_data):
    """Reconstructs a player from saved json_data as the correct subclass
    (DomesticPlayer/InternationalPlayer), instead of the base Player class,
    so nationality/player_type survive a pool-snapshot round trip - e.g.
    instantiate_players() rebuilding fresh Player objects to start an
    auction. json_data predating this field defaults to Domestic.
    """
    cls = PLAYER_TYPE_CLASSES.get(json_data.get("player_type", "Domestic"), DomesticPlayer)
    return cls(player_id, json_data)