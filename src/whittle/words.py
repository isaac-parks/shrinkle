import pickle
import random
import re
from pathlib import Path
from time import sleep

import requests as req

from whittle.cache import Cache, CTypes
from whittle.classes import Word
from whittle.constants import WORD_FILE_PATH, WORD_RANGE


def fetch_words():
    url = "https://raw.githubusercontent.com/isaac-parks/scrabble/refs/heads/master/dictionary.txt"
    res = req.get(url)
    if res.status_code != 200:
        return None

    raw_string = res.content.decode()
    words = raw_string.split("\n")
    words.append("a")
    words.append("i")
    for w in words:
        Cache.add(w.lower())

    return clean_words(words)


def clean_words(words):
    clean = set()
    for word in words:
        if len(word) in range(3, 7):
            clean.add(word.lower())

    return list(clean)


def remove_words_from_file(words_to_remove):
    words = []
    with open(WORD_FILE_PATH, "rb") as word_pkl:
        words = pickle.load(word_pkl)

    for word in words_to_remove:
        words.remove(word)

    with open(WORD_FILE_PATH, "wb") as word_pkl:
        pickle.dump(words, word_pkl)


def lookup_word_from_api(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    res = req.get(url)
    match res.status_code:
        case 429:
            # Too many requests, wait a good bit before trying again
            return lookup_word_from_api(word)
        case 404:
            return None

    if "application/json" not in res.headers.get("Content-Type", ""):
        # Should probably log that something weird happend, this could cause big problems
        return None

    return res.json()[0]


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

    return Word(candidates[0]), Word(candidates[1])


def slice(word, i):
    return (word[:i] + word[i + 1 :]).strip()
