from .abstract_wordle import AbstractWordle
from .dict_loader import get_possible_words, get_accepted_words, get_today_wordle_word
from .wordle_util import wordle_compare
import random

class Wordle(AbstractWordle):
    def __init__(self, data_path, use_real_word=False):
        if use_real_word:
            self.word = get_today_wordle_word()
        else:
            self.word = random.choice(get_possible_words(data_path))
        self.accepted_words = get_accepted_words(data_path)
        self.attempts = 0

    def try_word(self, guess):
        if guess not in self.accepted_words:
            return {
                "valid": False,
            }

        self.attempts += 1

        result = wordle_compare(guess, self.word)
        out = {
            "valid": True,
            "result": result,
        }
        
        if self.attempts >= 6:
            out |= { "correct": self.word }

        return out