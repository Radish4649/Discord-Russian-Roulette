import random


class Game:
    def __init__(self, id_, size: int = 6, number: int = 1, kick: bool = False):
        self.id = id_
        self.game = random.sample(range(1, size+1), k=number)
        self.size = size
        self.number = number
        self.kick_game = kick
        self.dead_players = []

    def __str__(self):
        return "game: {}\nkick game: {}\n dead players: {}".format(
            self.game, self.kick_game, self.dead_players
        )

    def shoot(self, shots, user):
        for current_shot in range(0, shots):
            self.game = list(map(lambda x: x - 1, self.game))
            if 0 in self.game:
                self.dead_players.append(user)
                self.game = list(filter(lambda x: x != 0, self.game))
                self.number = self.number - 1
                return True, current_shot + 1, self.number
        return False, shots, self.number


# this program returns the relevant code for that channel
def get_code(cxt):
    return str(cxt.guild) + " " + str(cxt.channel)
