import random


# this program returns the relevant code for that channel
def get_code(cxt):
    return str(cxt.guild) + " " + str(cxt.channel)


# sets the game settings object to default
def reset():
    return {"game": [], "in_progress": 0}

# eventually {"game": [], "in_progress": 0, "kick_mode": 0}
