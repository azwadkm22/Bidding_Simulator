from Player import Player
from Team import Team, printTeamPositionAndOrderDetails, printTeamPositionAndOrderSummary
from StartingEleven import StartingEleven
from UtilityBasedBidder import UtilityBasedBidder
import random



players = [None for _ in range(100)]
# players[0] = Player("Top Priority Player", 20, 98, 50, "Bowler", 50, "Right", "Spinner", None, "Low Order")

# players[1] = Player("Good Opening Batter", 90, 30, 50, "Batsmen", 50, "Left", None, None, "Opener")
# players[2] = Player("Mid Opening Batter", 75, 30, 50, "Batsmen", 50, "Right", None, None, "Opener")
players[3] = Player("Bad Opening Batter", 55, 30, 50, "Batsmen", 50, "Left", None, None, "Opener")

players[4] = Player("Good Wicketkeeper", 90, 30, 50, "Wicketkeeper", 50, "Left", None, None, "Top Order")
players[5] = Player("Mid Wicketkeeper", 75, 30, 50, "Wicketkeeper", 50, "Left", None, None, "Top Order")
players[6] = Player("Bad Wicketkeeper", 55, 30, 50, "Wicketkeeper", 50, "Left", None, None, "Top Order")

players[7] = Player("Good Top Order Batter", 90, 30, 50, "Batsmen", 50, "Left", None, None, "Top Order")
players[8] = Player("Mid Top Order Batter", 75, 30, 50, "Batsmen", 50, "Right", None, None, "Top Order")
players[9] = Player("Bad Top Order Batter", 55, 30, 50, "Batsmen", 50, "Left", None, None, "Top Order")


# players[10] = Player("Good Mid Order Batter", 90, 30, 50, "Batsmen", 50, "Left", None, None, "Middle Order")
# players[11] = Player("Mid Mid Order Batter", 75, 30, 50, "Batsmen", 50, "Right", None, None, "Middle Order")
# players[12] = Player("Bad Mid Order Batter", 55, 30, 50, "Batsmen", 50, "Left", None, None, "Middle Order")

# players[13] = Player("Good Low Order Batter", 90, 30, 50, "Batsmen", 50, "Left", None, None, "Low Order")
# players[14] = Player("Mid Low Order Batter", 75, 30, 50, "Batsmen", 50, "Right", None, None, "Low Order")
players[15] = Player("Bad Low Order Batter", 55, 30, 50, "Batsmen", 50, "Left", None, None, "Low Order")


# players[16] = Player("Good Pacer", 30, 90, 50, "Bowler", 50, "Left", "Pacer", None, "Low Order")
players[17] = Player("Mid Pacer", 30, 70, 50, "Bowler", 50, "Left", "Pacer", None, "Low Order")
players[18] = Player("Bad Pacer", 30, 55, 50, "Bowler", 50, "Left", "Pacer", None, "Low Order")

# players[19] = Player("Good Spinner", 30, 90, 50, "Bowler", 50, "Left", "Spinner", None, "Low Order")
players[20] = Player("Mid Spinner", 30, 70, 50, "Bowler", 50, "Left", "Spinner", None, "Low Order")
players[21] = Player("Bad Spinner", 30, 55, 50, "Bowler", 50, "Left", "Spinner", None, "Low Order")


# players[22] = Player("Good Allrounder Spinner", 90, 90, 50, "Allrounder", 50, "Left", "Spinner", None, "Middle Order")
players[23] = Player("Mid Allrounder Spinner", 70, 70, 50, "Allrounder", 50, "Left", "Spinner", None, "Middle Order")
players[24] = Player("Bad Allrounder Spinner", 40, 45, 50, "Allrounder", 50, "Left", "Spinner", None, "Middle Order")

# players[25] = Player("Good Allrounder Pacer", 90, 70, 50, "Allrounder", 50, "Left", "Pacer", None, "Middle Order")
players[26] = Player("Mid Allrounder Pacer", 70, 70, 50, "Allrounder", 50, "Left", "Pacer", None, "Middle Order")
players[27] = Player("Bad Allrounder Pacer", 40, 45, 50, "Allrounder", 50, "Left", "Pacer", None, "Middle Order")

# players[28] = Player("Good Pacer 2", 30, 90, 50, "Bowler", 50, "Left", "Pacer", None, "Low Order")
players[29] = Player("Mid Pacer 2", 30, 70, 50, "Bowler", 50, "Left", "Pacer", None, "Low Order")
players[30] = Player("Bad Pacer 2", 30, 55, 50, "Bowler", 50, "Left", "Pacer", None, "Low Order")

# players[31] = Player("Good Spinner 2", 35, 90, 50, "Bowler", 50, "Left", "Spinner", None, "Low Order")
players[32] = Player("Mid Spinner 2", 30, 70, 50, "Bowler", 50, "Left", "Spinner", None, "Low Order")
players[33] = Player("Bad Spinner 2", 30, 55, 50, "Bowler", 50, "Left", "Spinner", None, "Low Order")


# players[34] = Player("Good Top Order Batter 2", 90, 30, 50, "Batsmen", 50, "Left", None, None, "Top Order")
# players[35] = Player("Mid Top Order Batter 2", 75, 30, 50, "Batsmen", 50, "Right", None, None, "Top Order")
# players[36] = Player("Bad Top Order Batter 2", 55, 30, 50, "Batsmen", 50, "Left", None, None, "Top Order")


# players[37] = Player("Good Mid Order Batter 2", 90, 30, 50, "Batsmen", 50, "Left", None, None, "Middle Order")
# players[38] = Player("Mid Mid Order Batter 2", 75, 30, 50, "Batsmen", 50, "Right", None, None, "Middle Order")
# players[39] = Player("Bad Mid Order Batter 2", 55, 30, 50, "Batsmen", 50, "Left", None, None, "Middle Order")


# players[40] = Player("Good Opening Batter 2", 90, 30, 50, "Batsmen", 50, "Left", None, None, "Opener")
players[41] = Player("Mid Opening Batter 2", 75, 30, 50, "Batsmen", 50, "Right", None, None, "Opener")
players[42] = Player("Bad Opening Batter 2", 55, 30, 50, "Batsmen", 50, "Left", None, None, "Opener")

# Testing Odd cases

# players[43] = Player("Good Opening Batter 3", 90, 30, 50, "Batsmen", 50, "Left", None, None, "Opener")
# players[44] = Player("Good Top Order Batter 3", 97, 30, 50, "Batsmen", 50, "Left", None, None, "Top Order")

# players[45] = Player("Good Top Order Batter 4", 95, 30, 50, "Batsmen", 50, "Left", None, None, "Top Order")

# players[46] = Player("Good Top Order Batter 5", 92, 30, 50, "Batsmen", 50, "Left", None, None, "Top Order")

# players[47] = Player("Good Low Order Batter 5", 92, 30, 50, "Batsmen", 50, "Left", None, None, "Low Order")


# players[48] = Player("Good Wicketkeeper 2", 90, 30, 50, "Wicketkeeper", 50, "Left", None, None, "Top Order")

# players[49] = Player("Good Wicketkeeper 3", 90, 30, 50, "Wicketkeeper", 50, "Left", None, None, "Middle Order")

# players[50] = Player("Good Wicketkeeper 4", 90, 30, 50, "Wicketkeeper", 50, "Left", None, None, "Low Order")
# players[51] = Player("Good Opening Wicketkeeper 1", 90, 30, 50, "Wicketkeeper", 50, "Left", None, None, "Opener")
# players[52] = Player("Good Opening Wicketkeeper 2", 90, 30, 50, "Wicketkeeper", 50, "Left", None, None, "Opener")


players[53] = Player("Good Allrounder BWL Spinner", 80, 89, 50, "Allrounder", 50, "Left", "Spinner", None, "Middle Order")
players[54] = Player("Good Allrounder BAT Pacer", 80, 80, 50, "Allrounder", 50, "Left", "Pacer", None, "Middle Order")
players[55] = Player("Good Allrounder BAT Spinner", 89, 80, 50, "Allrounder", 50, "Left", "Spinner", None, "Middle Order")
players[56] = Player("BEST Allrounder BAT Spinner", 95, 95, 50, "Allrounder", 50, "Left", "Spinner", None, "Middle Order")

debugTeam1 = Team("Debug Team1")
debugTeam2 = Team("Debug Team2")

utbidder = UtilityBasedBidder(debugTeam1, 100, "")
# debugTeam3 = Team("Debug Team3")

for player in players:
    if(player != None):
        pick = random.choice([0, 1])
        # if pick == 0:
        
        sim = utbidder.compareWithOthers(10, player)
        debugTeam1.addPlayer(player)
            # print(s)
        print()
    #            print(s)
#            s.printSummary()
        # elif pick == 1:
        #     debugTeam2.addPlayer(player)
        # # else:
        #     debugTeam3.addPlayer(player)
        # debugTeam.addPlayer(player)

# debugTeam1.printTeamData()

# printTeamPositionAndOrderSummary(debugTeam)

# startingDebug = StartingEleven()

# startingDebug.createStartingEleven(debugTeam1)

# startingDebug.printTeamScore()

# startingDebug.printBenchedPlayers()


# startingDebug2 = StartingEleven()

# startingDebug2.createStartingEleven(debugTeam2)

# startingDebug2.printBenchedPlayers()


# startingDebug3 = StartingEleven()

# startingDebug3.createStartingEleven(debugTeam3)