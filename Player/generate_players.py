import json
from pathlib import Path
from Player.player import Player


def get_list_of_players(n):
    # Always generate a fresh pool. Previously this cached to a shared
    # relative-path file across all runs/sessions (and the cache-write path
    # was itself broken by an unpacking bug), which would leak players
    # between otherwise-independent game sessions.
    return generate_N_player_list(n)

def generate_N_player_list(n):
    list_of_players = []

    for i in range(n):
        new_player = Player(i)
        list_of_players.append(new_player)
    return list_of_players

def generate_player_list_from_JSON(generated_players_json, n):
    list_of_players = []

    for i in range(n):
        new_player = Player(player_id=i, json_data=generated_players_json[f"{i}"])
        list_of_players.append(new_player)

    return list_of_players

def save_player_list_to_JSON(list_of_players, file_path):
    data = {str(p.player_id): p.get_JSON_data() for p in list_of_players}
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def load_player_list_from_JSON(file_path, n):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return generate_player_list_from_JSON(data, n)
