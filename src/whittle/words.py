import random

import requests as req

from whittle.cache import Cache, CTypes
from whittle.classes import Word
from whittle.settings import WORD_RANGE


def get_raw_word_list():
    url = "https://raw.githubusercontent.com/isaac-parks/scrabble/refs/heads/master/dictionary.txt"
    res = req.get(url)
    if res.status_code != 200:
        return None

    raw_string = res.content.decode()
    words = raw_string.split("\n")
    words.append("a")
    words.append("i")

    return words


def get_selectable_words():
    all_words = get_raw_word_list()
    for w in all_words: # ????????
        Cache.add(w.lower()) # ???????

    return clean_words(all_words)


def clean_words(words):
    clean = set()
    for word in words:
        if len(word) in range(3, 7):
            clean.add(word.lower())

    return list(clean)


def lookup_word(word):
    if word == "":  # "" Is the final solution for the puzzle, so it is always valid
        return True

    cache = Cache()
    cache_lookup = cache.lookup(word)
    match cache_lookup:
        case CTypes.VALID_WORD:
            return True
        case CTypes.CACHE_MISS:
            return False

    return False


def select_words(words):
    candidates = []
    while len(candidates) != 2:
        new_candidate = random.choice(words)
        if len(candidates) == 1:
            first_word = candidates[0]
            if len(first_word) + len(new_candidate) not in range(
                WORD_RANGE[0], WORD_RANGE[1]
            ):
                candidates = []
                continue

        if new_candidate:
            candidates.append(new_candidate)
    return Word(candidates[0], True), Word(candidates[1], True)


def slice(word, i):
    return (word[:i] + word[i + 1 :]).strip()
