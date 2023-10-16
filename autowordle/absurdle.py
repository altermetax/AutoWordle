from .abstract_wordle import AbstractWordle
from .dict_loader import get_possible_words, get_accepted_words, get_today_wordle_word
from .wordle_util import absurdle_step

class Absurdle(AbstractWordle):
    def __init__(self, data_path):
        self.remaining_words = get_possible_words(data_path)
        self.accepted_words = get_accepted_words(data_path)

    def try_word(self, guess):
        if guess not in self.accepted_words:
            return {
                "valid": False,
            }

        (groups, best_answer) = absurdle_step(guess, self.remaining_words)

        self.remaining_words = groups[best_answer]

        return {
            "valid": True,
            "result": best_answer
        }
