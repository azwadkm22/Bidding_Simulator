
def get_player_subset(playerList, role):
    subList = []
    if role == "Opener":
        for player in playerList:
            if player.batting_order == "Opener":
                subList.append(player)
        return subList
    
    elif role == "Wicketkeeper":
        for player in playerList:
            if player.position == "Wicketkeeper":
                subList.append(player)
        return subList
    
    elif role == "Allrounder":
        for player in playerList:
            if player.position == "Allrounder":
                subList.append(player)
        return subList
    
    elif role == "Spinner":
        for player in playerList:
            if (player.position == "Bowler" or player.position == "Allrounder") and player.bowling_type == "Spinner":
                subList.append(player)
        return subList

    elif role == "Pacer":
        for player in playerList:
            if (player.position == "Bowler" or player.position == "Allrounder") and player.bowling_type == "Pacer":
                subList.append(player)
        return subList
    return subList
        

def find_top_N_player_in_category(playerList, n, category):
    # One case left to handle what if n is bigger than sublist
    if(category == "Fame"):
        playerList = sorted(playerList, key=lambda Player: Player.fame, reverse=True)
        TopNPlayers = playerList[:n]
        return TopNPlayers

    elif(category == "Batting"):
        playerList = sorted(playerList, key=lambda Player: Player.batting, reverse=True)
        TopNPlayers = playerList[:n]
        return TopNPlayers
    
    elif(category == "Bowling"):
        playerList = sorted(playerList, key=lambda Player: Player.bowling, reverse=True)
        TopNPlayers = playerList[:n]
        return TopNPlayers
    
    elif(category == "Price"):
        playerList = sorted(playerList, key=lambda Player: Player.estimated_price, reverse=True)
        TopNPlayers = playerList[:n]
        return TopNPlayers
    
    elif(category == "Pacer"):
        subList = get_player_subset(playerList, "Pacer")
        subList = sorted(subList, key=lambda Player: Player.bowling, reverse=True)
        TopNPlayers = subList[:n]
        return TopNPlayers
    
    elif(category == "Spinner"):
        subList = get_player_subset(playerList, "Spinner")
        subList = sorted(subList, key=lambda Player: Player.bowling, reverse=True)
        TopNPlayers = subList[:n]
        return TopNPlayers
    
    elif(category == "Wicketkeeper"):
        subList =  get_player_subset(playerList, "Wicketkeeper")
        subList = sorted(subList, key=lambda Player: Player.batting, reverse=True)
        TopNPlayers = subList[:n]
        return TopNPlayers

    elif(category == "Allrounder"):
        subList =  get_player_subset(playerList, "Allrounder")
        subList = sorted(subList, key=lambda Player: (Player.batting + Player.bowling )/2, reverse=True)
        TopNPlayers = subList[:n]
        return TopNPlayers
    
    elif(category == "Opener"):
        subList =  get_player_subset(playerList, "Opener")
        subList = sorted(subList, key=lambda Player: Player.batting, reverse=True)
        TopNPlayers = subList[:n]
        return TopNPlayers

def find_players_with_stats_above(playerList, stat, value):
    lop = []
    for player in playerList:
        if(stat == "Batting"):
            if player.batting > value:
                lop.append(player)

        elif(stat == "Bowling"):
            if player.bowling > value:
                lop.append(player)

        elif(stat == "Allrounder"):
            if (player.batting + player.bowling)/2 > value:
                lop.append(player)

        elif(stat == "Spin"):
            if player.bowling > value and player.bowling_type == "Spinner":
                lop.append(player)

        elif(stat == "Pace"):
            if player.bowling > value and player.bowling_type == "Pacer":
                lop.append(player)
    return lop


def find_players_above_rating(playerList, rating):
    players_above_rating = set()
    for player in playerList:
        if player.batting > rating or player.bowling > rating:
            players_above_rating.add(player)

    return players_above_rating