import random
import time
from Utils.showcase_utils import showcase_player
from Player.player_generation_stats import PlayerGenStat
from Team.team_generation_stats import TeamGenStat

class BiddingSimulation:
    def __init__(self, bidder_list, player_generation: PlayerGenStat, team_generation: TeamGenStat):
        self.team_generation = team_generation
        self.player_generation = player_generation
        self.bidder_list = bidder_list
        self.list_of_unsold_players = player_generation.list_of_players
        self.highest_price = 0

    def simulate_bidding(self, sleep_time=0):
        unsold_players = []
        for p in self.list_of_unsold_players:
            showcase_player(p, self.player_generation)
            not_sold = True
            placed_bid_this_round = False
            print("The player is now going up for bidding.")
            time.sleep(sleep_time)
            current_bidder = 0
            bid_counter = 0
            running_price = 10
            run = 0

            if p in self.team_generation.rivals_for_players.keys() :
                print("Teams eyeing him: ", self.team_generation.rivals_for_players[p])
            while(not_sold):
                # input()
                print("Reminder to everyone", p.name, "'s current price is", running_price)
                if(bid_counter == 0):
                    print("Do I get a bid from anyone?")
                    time.sleep(sleep_time)
                    run = run + 1
                if(bid_counter == 1):
                    print("Going once.")
                    time.sleep(sleep_time)
                if(bid_counter == 2):
                    print("Going Twice..")
                    time.sleep(sleep_time)
                if(bid_counter == 3):
                    print("Going Thrice...")
                    print("")
                    print("#SOLD SOLD SOLD#")
                    print(p.name, "sold to", current_bidder.name, "for", running_price, "(", p.estimated_price, ")")
                    print("#SOLD SOLD SOLD#")
                    print("")
                    current_bidder.subtractPrice(running_price)
                    not_sold = False
                    p.setSellingPrice(running_price)
                    current_bidder.addPlayerToTeam(p)
                    self.highest_price = max(self.highest_price, running_price)

                    time.sleep(sleep_time * 2)
                if(run > 2):
                    print(p.name, "remains unsold.")
                    not_sold = False
                    unsold_players.append(p)
                    time.sleep(sleep_time)
                    continue

                placed_bid_this_round = False
                for bidder in self.bidder_list:
                    print(bidder.name, bidder.trait, f"-UTILITY: {bidder.playerUtility}")

                # input()
                random.shuffle(self.bidder_list)
                for bidder in self.bidder_list:
                    if bidder != current_bidder:
                        if bidder.placeBid(p, running_price+5) == 1:
                            if bid_counter == 0:
                                print("We get a bid from", bidder.name)
                            if bid_counter == 1:
                                print("We get another bid from", bidder.name)
                            if bid_counter == 2:
                                print("Another count, and he would have been sold to", current_bidder.name, "but we have a bid from", bidder.name)
                            placed_bid_this_round = True
                            running_price = running_price + random.choice([2, 3, 4, 5])
                            bid_counter = 1
                            current_bidder = bidder
                            
                if(placed_bid_this_round == False and bid_counter != 0):
                    bid_counter =  bid_counter +1

        self.list_of_unsold_players = unsold_players
