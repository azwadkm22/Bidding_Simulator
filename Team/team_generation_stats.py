from Player.player_generation_stats import PlayerGenStat
from Team.shortlister import ShortList, makeShortList

class TeamGenStat:
    def __init__(self, team_list, player_generation: PlayerGenStat):
        self.team_list = team_list
        self.team_short_list, self.rivals_for_players = makeShortList(list(player_generation.players_above_80), team_list)