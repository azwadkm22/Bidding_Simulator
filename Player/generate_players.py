import json
import random
from pathlib import Path
from Player.player import DomesticPlayer, InternationalPlayer, build_player


def get_list_of_players(n, international_count=0):
    # Always generate a fresh pool. Previously this cached to a shared
    # relative-path file across all runs/sessions (and the cache-write path
    # was itself broken by an unpacking bug), which would leak players
    # between otherwise-independent game sessions.
    return generate_N_player_list(n, international_count)

def generate_N_player_list(n, international_count=0):
    # Which player_ids become International is shuffled rather than just the
    # first/last `international_count` ids, so they aren't clustered at one
    # end of anything sorted by player_id (generation order, before the
    # caller's own price sort).
    international_count = max(0, min(international_count, n))
    is_international = [True] * international_count + [False] * (n - international_count)
    random.shuffle(is_international)

    list_of_players = []
    for i in range(n):
        player_class = InternationalPlayer if is_international[i] else DomesticPlayer
        new_player = player_class(i)
        list_of_players.append(new_player)
    return list_of_players

def generate_player_list_from_JSON(generated_players_json, n):
    list_of_players = []

    for i in range(n):
        new_player = build_player(i, generated_players_json[f"{i}"])
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
