import pickle
from enum import Enum
from pathlib import Path

from whittle.settings import WORD_CACHE_FILE


class CTypes(Enum):
    VALID_WORD = 0
    CACHE_MISS = 2


class Cache:
    _word_cache = set()
    _cache_configured = False

    def __init__(self):
        if not self._cache_configured:
            self.configure_cache()

    @staticmethod
    def configure_cache():
        if Cache._cache_configured:
            return
        from whittle.words import get_raw_word_list
        words = set([w.lower() for w in get_raw_word_list()])
        Cache._word_cache = words
        Cache._cache_configured = True

    @staticmethod
    def save_cache():
        path = WORD_CACHE_FILE
        p = Path(path)
        p.touch(exist_ok=True)
        with open(path, "wb") as file:
            pickle.dump(Cache._word_cache, file)

        return True

    @staticmethod
    def lookup(word):
        if not Cache._cache_configured:
            Cache.configure_cache()
        if word in Cache._word_cache:
            return CTypes.VALID_WORD
        else:
            return CTypes.CACHE_MISS

    @staticmethod
    def add(word):
        if not Cache._cache_configured:
            Cache.configure_cache()

        Cache._word_cache.add(word)
