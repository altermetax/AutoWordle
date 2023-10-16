# Given a guess and a correct word, generate the result as a tuple of 5 strings representing colors
def wordle_compare(guess, correct_word):
    result = ["gray", "gray", "gray", "gray", "gray"]
    for i in range(len(correct_word)):
        if correct_word[i] == guess[i]:
            result[i] = "green"
        else:
            for j in range(len(guess)):
                if correct_word[i] == guess[j] and result[j] == "gray":
                    result[j] = "yellow"
                    break

    return tuple(result)

# Given a word and a colored word (array of dictionaries with keys "letter" and "color"),
# returns whether the word fits the constraints
def wordle_check(word, colored_word):
    yellow_counts = {}
    gray_letters = []

    for i in range(len(colored_word)):
        letter = colored_word[i]["letter"]
        color = colored_word[i]["color"]

        if color == "green":
            if word[i] != letter:
                return False
        elif color == "yellow":
            if word[i] == letter:
                return False
            if letter in yellow_counts:
                yellow_counts[letter] += 1
            else:
                yellow_counts[letter] = 1
        elif color == "gray":
            gray_letters.append(letter)

    for letter in gray_letters:
        if letter not in yellow_counts:
            for i in range(len(word)):
                if word[i] == letter and colored_word[i]["color"] != "green":
                    return False

    for letter in yellow_counts:
        count = 0
        for i in range(len(word)):
            if word[i] == letter and colored_word[i]["color"] != "green":
                count += 1
        if count < yellow_counts[letter]:
            return False
        
    return True

# Given two color arrays, return -1, 0 or 1 based on Absurdle criteria.
# In order of priority, these criteria are:
# Amount of greens
# Amount of yellows
# Alphabetical-like order, where green is A, yellow is B, gray is C
def compare_color_arrays(a, b):
    # Amount of greens
    agreen = a.count("green")
    bgreen = b.count("green")
    if agreen > bgreen:
        return 1
    elif agreen < bgreen:
        return -1
    
    # Amount of yellows
    ayellow = a.count("yellow")
    byellow = b.count("yellow")
    if ayellow > byellow:
        return 1
    elif ayellow < byellow:
        return -1
    
    # Alphabetical order
    for i in range(len(a)):
        if a[i] == "green" and b[i] != "green":
            return 1
        elif a[i] != "green" and b[i] == "green":
            return -1
        elif a[i] == "yellow" and b[i] == "gray":
            return 1
        elif a[i] == "gray" and b[i] == "yellow":
            return -1
        
    return 0

# Given a guess and a dictionary, returns the Absurdle groups for the guess and the best answer (as in: the one with the largest group)
def absurdle_step(guess, current_dictionary):
    # Group all remaining words based on what the outcome would be if they were the correct word
    # and pick the largest group
    groups = {}

    for word in current_dictionary:
        result = wordle_compare(guess, word)
        if result in groups:
            groups[result] += [word]
        else:
            groups[result] = [word]

    # Calculate best answer. If two groups are equally large, pick based on the keys, with criteria as in compare_color_arrays
    keys = list(groups.keys())
    best_answer = keys[0]
    for i in range(1, len(keys)):
        key = keys[i]
        if (len(groups[key]) > len(groups[best_answer]) or
                (len(groups[key]) == len(groups[best_answer]) and compare_color_arrays(key, best_answer) < 0)):
            best_answer = key

    return (groups, best_answer)
