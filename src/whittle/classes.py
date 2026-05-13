import requests as req


class Definition:
    def __init__(self, meaning_data):
        self.part_of_speech = meaning_data.get("partOfSpeech")
        self.definition = meaning_data.get("definition")
        self.example = meaning_data.get("example")

    def __str__(self):
        return self.definition


class Word:
    def __init__(self, word, sparce=False):
        if sparce:
            self.word = word
            self.definitions = []
            return
        word_data = self.lookup_word_from_api(word) or {}

        self.word = word_data.get("word", "")
        self.definitions = []
        for meaning in word_data.get("meanings", ""):
            if not meaning:
                continue
            for definition in meaning.get("definitions", ""):
                if not definition:
                    continue
                definition["partOfSpeech"] = meaning.get("partOfSpeech")
                self.definitions.append(Definition(definition))

    def __str__(self):
        return f'"{self.word}"'

    def lookup_word_from_api(self, word):
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        res = req.get(url)
        match res.status_code:
            case 429:
                return self.lookup_word_from_api(word)
            case 404:
                return None

        if "application/json" not in res.headers.get("Content-Type", ""):
            return None

        return res.json()[0]

    def __add__(self, val):
        if isinstance(val, Word):
            return len(self.word) + len(val.word)

        return len(self.word) + val


class Node:
    def __init__(self, value):
        self.value = value
        self.children = None

    def __repr__(self):
        return f"<node> {self.value}"

    def find_longest_path(self, next_total=-1):
        length = next_total + 1
        children = self.children if self.children else []
        if not children:
            return length

        totals = []
        for c in children:
            total = c.find_longest_path(next_total)
            totals.append(total)

        return max(totals)
