from Player.player_generation_stats import PlayerGenStat
from Player.player import Player


def print_title_board(title: str):
    print("########")
    print("")
    print(title)
    print("")
    print("########")

def print_summary_of_generation(genStat: PlayerGenStat):
    print_title_board("Best Wicketkeepers")
    for pl in genStat.top_eight_wicketkeepers:
        pl.printSkill()
    input()
    print_title_board("Best Batsmen")
    for pl in genStat.top_ten_batsmen:
        pl.printSummary()
    print_title_board("Best Bowlers")
    for pl in genStat.top_ten_bowlers:
        pl.printSummary()
    print_title_board("Best Allrounders")
    for pl in genStat.top_ten_allrounders:
        pl.printSummary()
    
    print_title_board("Best Openers")
    for pl in genStat.top_ten_openers:
        pl.printSummary()
    print_title_board("Best Spinners")
    for pl in genStat.top_ten_spinners:
        pl.printSummary()
    print_title_board("Best Pacers")
    for pl in genStat.top_ten_pacers:
        pl.printSummary()
    print_title_board("Most Famous")
    for pl in genStat.top_ten_famous:
        pl.printSummary()
    print_title_board("Most Expensive")
    for pl in genStat.top_ten_most_expensive:
        pl.printSummary()

    print_title_board("Now all the best players with score above 80")

    for player in genStat.players_above_80:
        player.printInLine()

    print("Total Players above 80: ", len(genStat.players_above_80))

    print(f'BatsmenAbove80: {len(genStat.players_above_80_batting)}')
    print(f'BowlersAbove80: {len(genStat.players_above_80_bowling)}')
    print(f'AllrounderAbove80: {len(genStat.players_above_80_allrounder)}')
    print(f'PacerAbove80: {len(genStat.players_above_80_pace)}')
    print(f'SpinnerAbove80: {len(genStat.players_above_80_spin)}')

def showcase_player(player: Player, genStat: PlayerGenStat):
    print_title_board("Next Player: " + player.name)
    if(player in genStat.top_ten_allrounders):
        print("He is one of the top contenders of this years best all rounder award.")

    elif(player in genStat.top_ten_batsmen):
        print("He is one of the top contenders of this years best batsmen award.")

    elif(player in genStat.top_ten_bowlers):
        print("He is one of the top contenders of this years best bowler award.")

    if(player in genStat.top_eight_wicketkeepers):
        print("He should be a regular in one of the teams for sure.")
    
    if(player in genStat.top_ten_pacers):
        print("Very few pacers out there with skills like his.")
    elif (player in genStat.top_ten_spinners):
        print("Just give him the ball and watch it spin all the way.")

    if (player in genStat.top_ten_openers):
        print("Which team will he open for this year.")

    if(player in genStat.top_ten_famous):
        print("He's got a lot of fans around the world.")

    print("He is well known as a", player.position)

    if(player.position == "Batsmen" or player.position == "Wicketkeeper"):
        # Add Traits based commentary here later
        if(player.batting > 90):
            print("Definitely one of the best batsmen I've ever seen playing.")
        elif(player.batting > 80):
            print("He's quite good with his footwork.")
        print("He's got a batting score of:", player.batting)
    
    elif(player.position == "Bowler"):
        # Add Traits based commentary here later
        if(player.bowling > 90):
            print("Definitely one of the best bowlers I've ever witnessed.")
        elif(player.bowling > 80):
            print("He's quite adept with his bowling.")
        print("He's got a bowling score of:", player.bowling)
    
    elif(player.position == "Allrounder"):
        # Add Traits based commentary here later
        if(player.bowling > 90 and player.batting > 90):
            print("Is there anything he's not good at?")
        elif(player.bowling > 80 and player.batting > 80):
            print("Good with the bowl and the bat.")

        print("He's got a batting score of: ", player.batting)
        print("He's got a bowling score of: ", player.bowling)
    
    if player.fielding > 90:
        print("He's also a terrific fielder. Nothing gets past him.")
    elif player.fielding > 80:
        print("His fielding skill is also remarkable")
    
    print(player.estimated_price)
    if(player.estimated_price > 100):
        print("I don't think any team is willing to let him go for a low price: ")
        print("If I had to say a price, I wouldn't suggest anything less than", int(player.estimated_price/10)*10, "Million")
    if(player.estimated_price < 50):
        print("What do you think, will he be bought this time?")
        print("If I had to say a price, I wouldn't suggest anything more than", (int(player.estimated_price/10)+1)*10, "Million")

def count_ratio(genStat: PlayerGenStat):
    bat = 0
    bowl = 0
    spin = 0
    pace = 0
    wk = 0
    allr = 0
    trainee = 0
    for player in genStat.list_of_players:
        if player.position == "Batsmen":
            bat = bat + 1
        elif player.position == "Wicketkeeper":
            wk = wk + 1
        elif player.position == "Allrounder":
            allr = allr + 1
        elif player.position == "Bowler":
            bowl = bowl + 1
            if player.bowling_type == "Spinner":
                spin = spin + 1
            if player.bowling_type == "Pacer":
                pace = pace + 1
        else:
            player.printSkill()
            trainee = trainee + 1

    print("Batsmen Count: ", bat)
    print("Wicketkeeper Count: ", wk)
    print("Allrounder Count: ", allr)
    print("Bowler Count: ", bowl)
    print("Spinner Count: ", spin)
    print("Pacer Count: ", pace)
    print("Trainee Count: ", trainee)