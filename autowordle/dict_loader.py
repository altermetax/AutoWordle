import os

cached = {}

def _get_words(filename):
    global cached
    if filename in cached:
        return cached[filename]
    else:
        with open(filename) as f:
            cached[filename] = [line.rstrip() for line in f]
        return cached[filename]

# Returns a list of all possible wordle words
def get_possible_words(root_path):
    return _get_words(os.path.join(root_path, "possible_words.txt"))

# Returns a list of all existing 5-letter words
def get_accepted_words(root_path):
    return _get_words(os.path.join(root_path, "accepted_words.txt"))