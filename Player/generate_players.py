import json
from Player.player import Player
from pathlib import Path
from Manager.player_manager import load_players


def get_list_of_players(n):
    file_path = Path("./generated/generated_players_data.json")
    if file_path.exists():
        generated_players = load_players()
        list_of_players = generate_player_list_from_JSON(generated_players, n)
    else:
        list_of_players, generated_players = generate_N_player_list(n)
        with open(file_path, 'w') as f:
            json.dump(generated_players, f, indent=4)

    return list_of_players

def generate_N_player_list(n):
    list_of_players = []
    generated_players = {}
    
    for i in range(n):
        new_player = Player(i)
        generated_players[i] = new_player.get_JSON_data()
        list_of_players.append(new_player)
    return list_of_players, generated_players

def generate_player_list_from_JSON(generated_players_json, n):
    list_of_players = []

    for i in range(n):
        new_player = Player(player_id=i, json_data=generated_players_json[f"{i}"])
        list_of_players.append(new_player)

    return list_of_players
    