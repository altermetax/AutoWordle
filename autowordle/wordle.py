from .abstract_wordle import AbstractWordle
import random

class Wordle(AbstractWordle):
    def __init__(self, possible_words, accepted_words):
        self.word = random.choice(possible_words)
        self.accepted_words = accepted_words
        self.attempts = 0

    def try_word(self, guess):
        if guess not in self.accepted_words:
            return {
                "valid": False,
            }

        self.attempts += 1

        result = ["gray", "gray", "gray", "gray", "gray"]
        for i in range(len(self.word)):
            if self.word[i] == guess[i]:
                result[i] = "green"
            else:
                for j in range(len(guess)):
                    if self.word[i] == guess[j] and result[j] != "green":
                        result[j] = "yellow"
                        break
        out = {
            "valid": True,
            "result": result,
        }
        
        if self.attempts >= 6:
            out |= { "correct": self.word }

        return out