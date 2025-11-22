from Team.team import Team


def findTeamStrength(team: Team):
    strength = []
    good_batsmen_count = 0
    good_allrounder_count = 0
    good_spinner_count = 0
    good_pacer_count = 0
    for player in team.playerList:
        if player.position == "Batsmen" or player.position == "Wicketkeeper":
            if player.batting >= 80:
                good_batsmen_count = good_batsmen_count + 1
        
        if player.position == "Allrounder":
            if player.batting >= 80 and player.bowling >= 80:
                good_allrounder_count = good_allrounder_count + 1
            elif player.batting >= 80:
                good_batsmen_count = good_batsmen_count + 1
            elif player.bowling >= 80:
                if player.bowling_type =="Pacer":
                    good_pacer_count = good_pacer_count + 1
                else:
                    good_spinner_count = good_spinner_count + 1
        
        if player.position == "Bowler":
            if player.bowling >= 80:
                if player.bowling_type =="Pacer":
                    good_pacer_count = good_pacer_count + 1
                else:
                    good_spinner_count = good_spinner_count + 1
        
    
    print("Good Batsmen: ", good_batsmen_count)
    print("Good Allrounder: ", good_allrounder_count)
    print("Good Spinner: ", good_spinner_count)
    print("Good Pacer: ", good_pacer_count)
        