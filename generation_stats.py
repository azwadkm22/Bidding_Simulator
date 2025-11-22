from player_list_utils import find_top_N_player_in_category, find_players_with_stats_above, find_players_above_rating


class GenerationStat:

    def __init__(self, list_of_players):
        self.list_of_players = list_of_players
        self.top_ten_batsmen = find_top_N_player_in_category(list_of_players, 10, "Batting")
        self.top_ten_bowlers = find_top_N_player_in_category(list_of_players, 10, "Bowling")
        self.top_ten_spinners = find_top_N_player_in_category(list_of_players, 10, "Spinner")
        self.top_ten_pacers = find_top_N_player_in_category(list_of_players, 10, "Pacer")
        self.top_eight_wicketkeepers = find_top_N_player_in_category(list_of_players, 24, "Wicketkeeper")
        self.top_ten_openers = find_top_N_player_in_category(list_of_players, 10, "Opener")
        self.top_ten_allrounders = find_top_N_player_in_category(list_of_players, 10, "Allrounder")
        self.top_ten_famous = find_top_N_player_in_category(list_of_players, 10, "Fame")
        self.top_ten_most_expensive = find_top_N_player_in_category(list_of_players, 10, "Price")

        self.players_above_80_batting = find_players_with_stats_above(list_of_players, "Batting", 80)
        self.players_above_80_bowling = find_players_with_stats_above(list_of_players, "Bowling", 80)
        self.players_above_80_spin = find_players_with_stats_above(list_of_players, "Spin", 80)
        self.players_above_80_pace = find_players_with_stats_above(list_of_players, "Pace", 80)
        self.players_above_80_allrounder = find_players_with_stats_above(list_of_players, "Allrounder", 80)
        self.players_above_80 = find_players_above_rating(list_of_players, 80)
        self.players_above_90 = find_players_above_rating(list_of_players, 90)