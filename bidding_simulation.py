import json
import random
import time
from pathlib import Path
from Utils.showcase_utils import showcase_player, showcase_player_UI
from Player.player_generation_stats import PlayerGenStat
from Team.team_generation_stats import TeamGenStat
from Bidders.user_bidder import UserBidder
from UI.market_window import show_market_status_window
from UI.player_window import show_player_info_in_window
from UI.team_squad_info_window import show_team_info_window
from UI.commentary_window import show_commentary_info_in_window
from UI.player_highlights_window import show_highlight_info_window
from Manager.player_manager import load_highlights

class BiddingSimulation:
    def __init__(self, user_bidder: UserBidder, bidder_list, player_generation: PlayerGenStat, team_generation: TeamGenStat):
        self.team_generation = team_generation
        self.player_generation = player_generation
        self.bidder_list = bidder_list
        self.list_of_unsold_players = player_generation.list_of_players
        self.highest_price = 0
        self.player_count = len(player_generation.list_of_players)
        self.user_bidder = user_bidder
        self.team_squad_data = {}
        self.player_sold_data = {}
        self.generation_highlights = {}

        for bd in bidder_list:
            self.team_squad_data[bd.name] = []
        self.team_squad_data[user_bidder.name] = []

        file_path = Path("./generated/players_highlights.json")

        if file_path.exists():
            self.generation_highlights = load_highlights()
        else:
            self.generation_highlights = self.player_generation.get_all_highlight_player_ids()
            with open(file_path, 'w') as f:
                json.dump(self.generation_highlights, f, indent=4)


    def simulate_bidding(self, sleep_time=0):
        auction_number = 0
        unsold_players = []
        comments = []
        for p in self.list_of_unsold_players:
            showcase_player(p, self.player_generation)
            not_sold = True
            placed_bid_this_round = False
            comments.append(f"{p.name} is now going up for bidding.")
            print("The player is now going up for bidding.")
            time.sleep(sleep_time)
            current_bidder = 0
            bid_counter = 0
            running_price = 10
            run = 0
            show_player_info_in_window(p.player_id)
            show_market_status_window(auction_number, self.player_count - auction_number, len(unsold_players))
            show_team_info_window(self.team_squad_data, self.player_sold_data)
            show_highlight_info_window(self.generation_highlights)
            if p in self.team_generation.rivals_for_players.keys() :
                comments.append(f"Teams eyeing him: {self.team_generation.rivals_for_players[p]}")
                print("Teams eyeing him: ", self.team_generation.rivals_for_players[p])

            # show_commentary_info_in_window(comments)
            while(not_sold):
                comments = []
                user_bid = ""
                comments.append(f"Reminder to everyone {p.name}'s current price is {running_price}")
                print("Reminder to everyone", p.name, "'s current price is", running_price)
                if(bid_counter == 0):
                    comments.append(f"Do I get a bid from anyone?")
                    print("Do I get a bid from anyone?")
                    if current_bidder != self.user_bidder:
                        user_bid = input("Place Bid?")
                    time.sleep(sleep_time)
                    run = run + 1
                if(bid_counter == 1):
                    comments.append(f"Going once.")
                    print("Going once.")
                    if current_bidder != self.user_bidder:
                        user_bid = input("Place Bid?")
                    time.sleep(sleep_time)
                if(bid_counter == 2):
                    comments.append(f"Going twice.")
                    print("Going Twice..")
                    if current_bidder != self.user_bidder:
                        user_bid = input("Place Bid?")
                    time.sleep(sleep_time)
                if(bid_counter == 3):
                    comments.append(f"Going thrice.")
                    comments.append(f"SOLD")
                    comments.append(f"{p.name} sold to {current_bidder.name}, for , {running_price}")
                    print("Going Thrice...")
                    print("")
                    print("#SOLD SOLD SOLD#")
                    print(p.name, "sold to", current_bidder.name, "for", running_price, "(", p.estimated_price, ")")
                    self.player_sold_data[p.player_id] = running_price
                    self.team_squad_data[current_bidder.name].append(p.player_id)
                    print("#SOLD SOLD SOLD#")
                    print("")
                    current_bidder.subtractPrice(running_price)
                    not_sold = False
                    p.setSellingPrice(running_price)
                    current_bidder.addPlayerToTeam(p)
                    self.highest_price = max(self.highest_price, running_price)
                    auction_number = auction_number + 1
                    time.sleep(sleep_time * 2)
                    continue

                if(run > 2):
                    print(p.name, "remains unsold.")
                    comments.append(f"{p.name} remains unsold.")
                    not_sold = False
                    unsold_players.append(p)
                    time.sleep(sleep_time)
                    auction_number = auction_number + 1
                    continue

                placed_bid_this_round = False
                
                if user_bid != "":
                    try:
                        if int(user_bid):
                            running_price = running_price + int(user_bid)
                            comments.append(f"We get a bid from {self.user_bidder.name}.")
                            comments.append(f"{p.name}'s current price is {running_price}")
                            print(f"We get a bid from {self.user_bidder.name}.")
                            print(f"{p.name}'s current price is {running_price}")
                            placed_bid_this_round = True
                            current_bidder = self.user_bidder
                            bid_counter = 1
                    except ValueError:
                        print("Exception: User bid invalid.")
                
                random.shuffle(self.bidder_list)
                for bidder in self.bidder_list:
                    if bidder != current_bidder:
                        if bidder.placeBid(p, running_price+5) == 1:
                            pre_text = ""
                            if bid_counter == 0:
                                pre_text = f"We get a bid from {bidder.name}"
                            if bid_counter == 1:
                                pre_text = f"We get another bid from {bidder.name}"
                            if bid_counter == 2:
                                pre_text = f"Another count, and he would have been sold to {current_bidder.name} but we have a bid from {bidder.name}"
                            placed_bid_this_round = True
                            increase = random.choice([2, 3, 4, 5])
                            running_price = running_price + increase

                            comments.append(f"{pre_text} with + {increase}")
                            comments.append(f"{p.name}'s current price is {running_price}")
                            print(f"{pre_text} with + {increase}")
                            print(f"{p.name}'s current price is {running_price}")
                            bid_counter = 1
                            current_bidder = bidder
                            
                if(placed_bid_this_round == False and bid_counter != 0):
                    bid_counter =  bid_counter +1

                show_commentary_info_in_window(comments)

        self.list_of_unsold_players = unsold_players

    def get_team_squad_data(self):
        return self.team_squad_data
    
    def get_player_sold_data(self):
        return self.player_sold_data