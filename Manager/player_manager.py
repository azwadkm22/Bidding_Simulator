# player_manager.py
import json

_players = None
_players_highlights = None 
def load_players():
    """Loads player.json only once (cached)."""
    global _players
    if _players is None:
        with open("generated/generated_players_data.json", "r") as f:
            _players = json.load(f)
    return _players

def load_highlights():
    global _players_highlights
    if _players_highlights is None:
        with open("generated/players_highlights.json", "r") as f:
            _players_highlights = json.load(f)
    return _players_highlights

def get_player(pid):
    """Get a single player by ID as int or str."""
    players = load_players()
    pid = str(pid)
    return players.get(pid)


def get_many(player_ids):
    """Convert a list of IDs → list of player dicts."""
    players = load_players()
    result = []
    for pid in player_ids:
        pid = str(pid)
        if pid in players:
            result.append(players[pid])
    return result
