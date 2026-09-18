import random
from Utils.probability_utils import get_probabilistic_answer

REGIONS = [
    "Dhaka",
    "Rajshahi",
    "Sylhet",
    "Barishal",
    "Khulna",
    "Chittagong",
    "Rangpur",
    "Cox's Bazar",
    "Cumilla",
    "Noakhali",
    "Dinajpur",
    "Jessore",
    "Mymensingh",
    "Bogura",
    "Brahmanbaria",
    "Tangail",
    "Gazipur",
    "Chandpur",
    "Rangamati",
    "Bandarban",
    "Padma",
    "Meghna",
    "Jamuna",
    "Surma",
    "Teesta",
    "Rupsha"
]

END_NAMES = [
    "Dynamites",
    "Bulls",
    "Titans",
    "Tigers",
    "Sixers",
    "Howlers",
    "Wolves",
    "Gladiators",
    "Riders",
    "Victorians",
    "Kings",
    "Rajahs",
    "Vipers",
    "Dragons",
    "Warriors",
    "Royals",
    "Knights",
    "Eagles",
    "Cobras",
    "Rhinos",
    "Sharks",
    "Strikers",
    "Chargers",
    "Challengers",
    "Blazers",
    "Storm",
]

START_NAMES = [
    "Stellar",
    "Royal",
    "Mighty",
    "Ferocious",
    "Blazing",
    "Fearless",
    "Rising",
    "United",
]

def new_name_pool():
    # Per-call copies so each game session drains its own pool instead of a
    # shared process-global one (which would run out across concurrent sessions).
    return {
        "regions": list(REGIONS),
        "start_names": list(START_NAMES),
        "end_names": list(END_NAMES),
    }

def createTeamName(pool=None):
    if pool is None:
        pool = new_name_pool()

    regions = pool["regions"]
    start_names = pool["start_names"]
    end_names = pool["end_names"]

    reg = random.choice(regions)
    regions.remove(reg)

    if len(start_names) > 0:
        if(get_probabilistic_answer(0.2)):
            start = random.choice(start_names)
            start_names.remove(start)
            return start + " " + reg

    end = random.choice(end_names)
    end_names.remove(end)
    return reg + " " + end


# for i in range(10):
#     print(createTeamName())
#
