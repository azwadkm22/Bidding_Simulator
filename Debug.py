from PlayerGenerator import Player
from TeamGenerator import Team, printTeamPositionAndOrderDetails, printTeamPositionAndOrderSummary
from StartingEleven import StartingEleven




players = [None for _ in range(43)]
players[0] = Player("Top Priority Player", 98, 30, 75, "Batsmen", 75, "Right", None, None, "Middle Order")

players[1] = Player("Good Opening Batter", 85, 30, 75, "Batsmen", 75, "Left", None, None, "Opener")
players[2] = Player("Mid Opening Batter", 75, 30, 75, "Batsmen", 75, "Right", None, None, "Opener")
players[3] = Player("Bad Opening Batter", 55, 30, 75, "Batsmen", 75, "Left", None, None, "Opener")

players[4] = Player("Good Wicketkeeper", 85, 30, 75, "Wicketkeeper", 75, "Left", None, None, "Top Order")
players[5] = Player("Mid Wicketkeeper", 75, 30, 75, "Wicketkeeper", 75, "Left", None, None, "Top Order")
players[6] = Player("Bad Wicketkeeper", 55, 30, 75, "Wicketkeeper", 75, "Left", None, None, "Top Order")

players[7] = Player("Good Top Order Batter", 85, 30, 75, "Batsmen", 75, "Left", None, None, "Top Order")
players[8] = Player("Mid Top Order Batter", 75, 30, 75, "Batsmen", 75, "Right", None, None, "Top Order")
players[9] = Player("Bad Top Order Batter", 55, 30, 75, "Batsmen", 75, "Left", None, None, "Top Order")


players[10] = Player("Good Mid Order Batter", 85, 30, 75, "Batsmen", 75, "Left", None, None, "Middle Order")
players[11] = Player("Mid Mid Order Batter", 75, 30, 75, "Batsmen", 75, "Right", None, None, "Middle Order")
players[12] = Player("Bad Mid Order Batter", 55, 30, 75, "Batsmen", 75, "Left", None, None, "Middle Order")

players[13] = Player("Good Low Order Batter", 85, 30, 75, "Batsmen", 75, "Left", None, None, "Low Order")
players[14] = Player("Mid Low Order Batter", 75, 30, 75, "Batsmen", 75, "Right", None, None, "Low Order")
players[15] = Player("Bad Low Order Batter", 55, 30, 75, "Batsmen", 75, "Left", None, None, "Low Order")


players[16] = Player("Good Pacer", 30, 85, 75, "Bowler", 75, "Left", "Pacer", None, "Low Order")
players[17] = Player("Mid Pacer", 30, 70, 75, "Bowler", 75, "Left", "Pacer", None, "Low Order")
players[18] = Player("Bad Pacer", 30, 55, 75, "Bowler", 75, "Left", "Pacer", None, "Low Order")

players[19] = Player("Good Spinner", 30, 85, 75, "Bowler", 75, "Left", "Spinner", None, "Low Order")
players[20] = Player("Mid Spinner", 30, 70, 75, "Bowler", 75, "Left", "Spinner", None, "Low Order")
players[21] = Player("Bad Spinner", 30, 55, 75, "Bowler", 75, "Left", "Spinner", None, "Low Order")


players[22] = Player("Good Allrounder Spinner", 85, 70, 75, "Allrounder", 75, "Left", "Spinner", None, "Middle Order")
players[23] = Player("Mid Allrounder Spinner", 70, 60, 75, "Allrounder", 75, "Left", "Spinner", None, "Middle Order")
players[24] = Player("Bad Allrounder Spinner", 40, 45, 75, "Allrounder", 75, "Left", "Spinner", None, "Middle Order")

players[25] = Player("Good Allrounder Pacer", 85, 70, 75, "Allrounder", 75, "Left", "Pacer", None, "Middle Order")
players[26] = Player("Mid Allrounder Pacer", 70, 60, 75, "Allrounder", 75, "Left", "Pacer", None, "Middle Order")
players[27] = Player("Bad Allrounder Pacer", 40, 45, 75, "Allrounder", 75, "Left", "Pacer", None, "Middle Order")

players[28] = Player("Good Pacer 2", 30, 85, 75, "Bowler", 75, "Left", "Pacer", None, "Low Order")
players[29] = Player("Mid Pacer 2", 30, 70, 75, "Bowler", 75, "Left", "Pacer", None, "Low Order")
players[30] = Player("Bad Pacer 2", 30, 55, 75, "Bowler", 75, "Left", "Pacer", None, "Low Order")

players[31] = Player("Good Spinner 2", 30, 85, 75, "Bowler", 75, "Left", "Spinner", None, "Low Order")
players[32] = Player("Mid Spinner 2", 30, 70, 75, "Bowler", 75, "Left", "Spinner", None, "Low Order")
players[33] = Player("Bad Spinner 2", 30, 55, 75, "Bowler", 75, "Left", "Spinner", None, "Low Order")


players[34] = Player("Good Top Order Batter 2", 85, 30, 75, "Batsmen", 75, "Left", None, None, "Top Order")
players[35] = Player("Mid Top Order Batter 2", 75, 30, 75, "Batsmen", 75, "Right", None, None, "Top Order")
players[36] = Player("Bad Top Order Batter 2", 55, 30, 75, "Batsmen", 75, "Left", None, None, "Top Order")


players[37] = Player("Good Mid Order Batter 2", 85, 30, 75, "Batsmen", 75, "Left", None, None, "Middle Order")
players[38] = Player("Mid Mid Order Batter 2", 75, 30, 75, "Batsmen", 75, "Right", None, None, "Middle Order")
players[39] = Player("Bad Mid Order Batter 2", 55, 30, 75, "Batsmen", 75, "Left", None, None, "Middle Order")


players[40] = Player("Good Opening Batter 2", 85, 30, 75, "Batsmen", 75, "Left", None, None, "Opener")
players[41] = Player("Mid Opening Batter 2", 75, 30, 75, "Batsmen", 75, "Right", None, None, "Opener")
players[42] = Player("Bad Opening Batter 2", 55, 30, 75, "Batsmen", 75, "Left", None, None, "Opener")


debugTeam = Team("Debug Team")

for player in players:
    debugTeam.addPlayer(player)

debugTeam.printTeamData()

printTeamPositionAndOrderSummary(debugTeam)

startingDebug = StartingEleven()

startingDebug.createStartingEleven(debugTeam)