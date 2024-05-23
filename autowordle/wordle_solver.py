from .dict_loader import get_possible_words, get_accepted_words
from .wordle_util import wordle_filter, wordle_groups
from math import sqrt, log2

class WordleSolver:
    def __init__(self, data_path, verbose=True):
        self.number_of_past_attempts = 0
        self.remaining_words = get_possible_words(data_path)
        self.accepted_words = get_accepted_words(data_path)
        self.verbose = verbose

    def get_guess(self, new_game_state):
        # Restrict remaining_words based on new data
        for colored_word in new_game_state:
            self.remaining_words = wordle_filter(self.remaining_words, colored_word)

        self.number_of_past_attempts += len(new_game_state)

        if len(self.remaining_words) == 0:
            return None
        
        if self.number_of_past_attempts == 0:
            # Hardcoded first word
            return {
                "word": "RAISE"
            }

        idxmin = None
        scoremin = 0

        for i, word in enumerate(self.remaining_words):
            groups = wordle_groups(word, self.remaining_words)
            total_size = len(self.remaining_words)
            n_groups = len(groups)

            mean = total_size / n_groups

            sum = 0
            for group in groups.values():
                sum += (len(group) - mean) ** 2

            std_deviation = sqrt(sum / n_groups)

            score = mean * std_deviation
            
            if self.verbose:
                print(f"Score for {word}: {score}")

            if idxmin is None or score < scoremin:
                idxmin = i
                scoremin = score
                if self.verbose:
                    print("Minimum score surpassed")

        answer = self.remaining_words[idxmin]

        if self.verbose:
            print(f"Responding with {answer}")

        return {
            "word": answer
        }

class SandersonWordleSolver:
    def __init__(self, data_path, verbose=True):
        self.number_of_past_attempts = 0
        self.remaining_words = get_possible_words(data_path)
        self.accepted_words = get_accepted_words(data_path)
        self.verbose = verbose

    def get_guess(self, new_game_state):
        # Restrict remaining_words based on new data
        for colored_word in new_game_state:
            self.remaining_words = wordle_filter(self.remaining_words, colored_word)

        self.number_of_past_attempts += len(new_game_state)

        if len(self.remaining_words) == 0:
            return None
        
        if self.number_of_past_attempts == 0:
            # Hardcoded first word
            return {
                "word": "RAISE"
            }

        idxmax = None
        scoremax = 0

        for i, word in enumerate(self.remaining_words):
            groups = wordle_groups(word, self.remaining_words)
            total_size = len(self.remaining_words)
            score = 0
            for group in groups.values():
                probability = len(group) / total_size
                score += -probability * log2(probability)
            
            if self.verbose:
                print(f"Score for {word}: {score}")

            if score >= scoremax:
                idxmax = i
                scoremax = score
                if self.verbose:
                    print("Maximum score surpassed")

        answer = self.remaining_words[idxmax]

        if self.verbose:
            print(f"Responding with {answer}")

        return {
            "word": answer
        }
