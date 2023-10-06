from .wordle import Wordle
from .absurdle import Absurdle

class SessionGameManager:
    games = {}
    next_id = 0

    def new_game(self, type, possible_words, accepted_words):
        id = self.next_id
        self.next_id += 1

        if type == "wordle":
            self.games[id] = Wordle(possible_words, accepted_words)
        elif type == "absurdle":
            self.games[id] = Absurdle(possible_words, accepted_words)

        return id

    def try_word(self, game_id, word):
        if game_id not in self.games:
            return None
        game = self.games[game_id]
        return game.try_word(word)