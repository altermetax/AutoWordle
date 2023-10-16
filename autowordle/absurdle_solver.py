from .dict_loader import get_possible_words
from .wordle_util import absurdle_step, wordle_check

class AbsurdleSolver:
    def __init__(self, data_path):
        self.remaining_words = get_possible_words(data_path)

    def get_guess(self, new_game_state):
        # Restrict remaining_words based on new data
        for colored_word in new_game_state:
            new_remaining_words = []
            for word in self.remaining_words:
                if wordle_check(word, colored_word):
                    new_remaining_words.append(word)
            self.remaining_words = new_remaining_words

        choices = {}
        for word in self.remaining_words:
            (groups, best_answer) = absurdle_step(word, self.remaining_words)
            choices[word] = (groups, len(groups[best_answer]))

        best_user_answer = min(choices, key=lambda k : choices[k][1])

        return {
            "word": best_user_answer
        }
