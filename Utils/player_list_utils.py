def get_player_subset(list_of_players, role: str):
    subList = []
    if role == "Opener":
        for player in list_of_players:
            if player.batting_order == "Opener":
                subList.append(player)
        return subList
    
    elif role == "Wicketkeeper":
        for player in list_of_players:
            if player.position == "Wicketkeeper":
                subList.append(player)
        return subList
    
    elif role == "Allrounder":
        for player in list_of_players:
            if player.position == "Allrounder":
                subList.append(player)
        return subList
    
    elif role == "Spinner":
        for player in list_of_players:
            if (player.position == "Bowler" or player.position == "Allrounder") and player.bowling_type == "Spinner":
                subList.append(player)
        return subList

    elif role == "Pacer":
        for player in list_of_players:
            if (player.position == "Bowler" or player.position == "Allrounder") and player.bowling_type == "Pacer":
                subList.append(player)
        return subList
    return subList
        

def find_top_N_player_in_category(list_of_players, n, category):
    # One case left to handle what if n is bigger than sublist
    if(category == "Fame"):
        list_of_players = sorted(list_of_players, key=lambda Player: Player.fame, reverse=True)
        top_N_players = list_of_players[:n]
        return top_N_players

    elif(category == "Batting"):
        list_of_players = sorted(list_of_players, key=lambda Player: Player.batting, reverse=True)
        top_N_players = list_of_players[:n]
        return top_N_players
    
    elif(category == "Bowling"):
        list_of_players = sorted(list_of_players, key=lambda Player: Player.bowling, reverse=True)
        top_N_players = list_of_players[:n]
        return top_N_players
    
    elif(category == "Price"):
        list_of_players = sorted(list_of_players, key=lambda Player: Player.estimated_price, reverse=True)
        top_N_players = list_of_players[:n]
        return top_N_players
    
    elif(category == "Pacer"):
        subList = get_player_subset(list_of_players, "Pacer")
        subList = sorted(subList, key=lambda Player: Player.bowling, reverse=True)
        top_N_players = subList[:n]
        return top_N_players
    
    elif(category == "Spinner"):
        subList = get_player_subset(list_of_players, "Spinner")
        subList = sorted(subList, key=lambda Player: Player.bowling, reverse=True)
        top_N_players = subList[:n]
        return top_N_players
    
    elif(category == "Wicketkeeper"):
        subList =  get_player_subset(list_of_players, "Wicketkeeper")
        subList = sorted(subList, key=lambda Player: Player.batting, reverse=True)
        top_N_players = subList[:n]
        return top_N_players

    elif(category == "Allrounder"):
        subList =  get_player_subset(list_of_players, "Allrounder")
        subList = sorted(subList, key=lambda Player: (Player.batting + Player.bowling )/2, reverse=True)
        top_N_players = subList[:n]
        return top_N_players
    
    elif(category == "Opener"):
        subList =  get_player_subset(list_of_players, "Opener")
        subList = sorted(subList, key=lambda Player: Player.batting, reverse=True)
        top_N_players = subList[:n]
        return top_N_players

def find_players_with_stats_above(list_of_players, stat, value):
    lop_above = []
    for player in list_of_players:
        if(stat == "Batting"):
            if player.batting > value:
                lop_above.append(player)

        elif(stat == "Bowling"):
            if player.bowling > value:
                lop_above.append(player)

        elif(stat == "Allrounder"):
            if (player.batting + player.bowling)/2 > value:
                lop_above.append(player)

        elif(stat == "Spin"):
            if player.bowling > value and player.bowling_type == "Spinner":
                lop_above.append(player)

        elif(stat == "Pace"):
            if player.bowling > value and player.bowling_type == "Pacer":
                lop_above.append(player)
    return lop_above


def find_players_above_rating(list_of_players, rating):
    players_above_rating = set()
    for player in list_of_players:
        if player.batting > rating or player.bowling > rating:
            players_above_rating.add(player)

    return players_above_rating


def get_player_ids_from_player_list(list_of_players):
    player_ids = []
    for p in list_of_players:
        player_ids.append(p.player_id)

    return player_ids
