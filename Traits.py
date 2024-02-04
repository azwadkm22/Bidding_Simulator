


class Trait:
    def __init__(self, typeOfTrait, name, attr):
        self.type = typeOfTrait
        self.name = name
        self.associated_attribute = attr



battingTraits = []
bowlingTraits = []
fieldingTraits = []

battingStats = ["Aggressiveness", "Power", "Attack Positioning","Composure", 
                "Vision", "Running Speed", "Stamina", "Defense",
                "Offside", "Legside", "Timing", "Footwork", "Straight"]

fieldingStats = ["Running Speed", "Stamina", "Catching", "Positioning", "Throwing", "Agility"]

pacingStats = ["Speed", "Accuracy", "Control", "Swing", "Yorker", "Bounce", "Stamina", "Seam", "Recovery"]
spinningStats = ["Spin", "Accuracy", "Control", "Turn", "Drift", "Dip", "Stamina", "Googly", "Doosra", "Slider", "Recovery"]

battingTraits.append(Trait("Batting", "Hard-Hitter", ["Aggressiveness", "Power"]))
battingTraits.append(Trait("Batting", "Showstopper", ["Vision", "Attack Positioning", "Power", "Composure"]))
battingTraits.append(Trait("Batting", "Mr. 360", ["Vision", "Offside", "Legside", "Straight"]))
battingTraits.append(Trait("Batting", "Run Machine", ["Running Speed", "Stamina"]))
battingTraits.append(Trait("Batting", "Ice Man", ["Defense", "Composure"]))
battingTraits.append(Trait("Batting", "The Wall", ["Defense", "Timing"]))
battingTraits.append(Trait("Batting", "Offside Technician", ["Offside", "Vision"]))
battingTraits.append(Trait("Batting", "Legside Maestro", ["Legside", "Vision"]))
battingTraits.append(Trait("Batting", "Straight Driver", ["Straight", "Vision"]))


bowlingTraits.append(Trait("Pacing", "Swing King", ["Swing"]))
bowlingTraits.append(Trait("Pacing", "Yorker Specialist", ["Yorker"]))
bowlingTraits.append(Trait("Bowling", "Silent Assassin", ["Control", "Recovery"]))
bowlingTraits.append(Trait("Spinning", "Spin Wizard", ["Spin", "Turn"]))
bowlingTraits.append(Trait("Bowling", "Gentle Giant", ["Accuracy", "Stamina"]))
bowlingTraits.append(Trait("Pacing", "Radar Bowler", ["Accuracy", "Control"]))
bowlingTraits.append(Trait("Pacing", "Bouncer Specialist", ["Bounce"]))
bowlingTraits.append(Trait("Pacing", "Speed Wizard", ["Speed"]))
bowlingTraits.append(Trait("Pacing", "Master Seamer", ["Seam"]))
bowlingTraits.append(Trait("Spinning", "Googly Guru", ["Googly"]))
bowlingTraits.append(Trait("Spinning", "Doosra Master", ["Doosra"]))
bowlingTraits.append(Trait("Spinning", "Slider Specialist", ["Slider"]))