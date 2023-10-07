from .abstract_wordle import AbstractWordle
from .dict_loader import get_possible_words, get_accepted_words, get_today_wordle_word
from .wordle_util import wordle_compare

class Absurdle(AbstractWordle):
    def __init__(self, data_path):
        self.remaining_words = get_possible_words(data_path)
        self.accepted_words = get_accepted_words(data_path)

    def try_word(self, guess):
        if guess not in self.accepted_words:
            return {
                "valid": False,
            }

        # Group all remaining words based on what the outcome would be if they were the correct word
        # and pick the largest group
        groups = {}

        for word in self.remaining_words:
            result = wordle_compare(guess, word)
            if result in groups:
                groups[result] += [word]
            else:
                groups[result] = [word]
        
        best_answer = max(groups, key=lambda k : len(groups[k]))

        self.remaining_words = groups[best_answer]

        return {
            "valid": True,
            "result": best_answer
        }
