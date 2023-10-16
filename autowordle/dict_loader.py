import os
import requests
import json
from datetime import datetime

cached = {}

def _get_lines(filename):
    global cached
    if filename in cached:
        return cached[filename]
    else:
        with open(filename) as f:
            cached[filename] = [line.rstrip() for line in f]
        return cached[filename]

# Returns a list of all possible wordle words
def get_possible_words(root_path):
    return _get_lines(os.path.join(root_path, "possible_words.txt"))

# Returns a list of all existing 5-letter words
def get_accepted_words(root_path):
    return _get_lines(os.path.join(root_path, "accepted_words.txt"))

# Returns today's actual wordle word, retrieved from the official API
def get_today_wordle_word():
    if get_today_wordle_word.cached is not None:
        return get_today_wordle_word.cached
    else:
        date_fmt = datetime.today().strftime("%Y-%m-%d")
        url = f"https://www.nytimes.com/svc/wordle/v2/{date_fmt}.json"
        resp = requests.get(url)

        if resp.status_code != 200:
            return None
        else:
            get_today_wordle_word.cached = json.loads(resp.text)["solution"].upper()
            return get_today_wordle_word.cached

get_today_wordle_word.cached = None
