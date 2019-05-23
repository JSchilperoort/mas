
from Agent import Agentt


class Coup:
    def __init__(self):
        self.n_players = 2

        self.players = list()
        self.set_players()

    def set_players(self):
        for i in range(self.n_players):
            property1, property2, property3 = 1, 2, 3
            self.players.append(Agentt(property1, property2, property3))
