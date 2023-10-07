# Given a guess and a correct word, generate the result as a tuple of 5 strings representing colors
def wordle_compare(guess, correct_word):
    result = ["gray", "gray", "gray", "gray", "gray"]
    for i in range(len(correct_word)):
        if correct_word[i] == guess[i]:
            result[i] = "green"
        else:
            for j in range(len(guess)):
                if correct_word[i] == guess[j] and result[j] != "green":
                    result[j] = "yellow"
                    break

    return tuple(result)
