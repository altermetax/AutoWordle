from .wordle import Wordle
from .absurdle import Absurdle

class SessionGameManager:
    games = {}
    next_id = 0

    def new_game(self, type, data_path):
        id = self.next_id
        self.next_id += 1

        if type == "wordle":
            self.games[id] = Wordle(data_path, False)
        elif type == "absurdle":
            self.games[id] = Absurdle(data_path)

        return id

    def try_word(self, game_id, word):
        if game_id not in self.games:
            return None
        game = self.games[game_id]
        return game.try_word(word)
