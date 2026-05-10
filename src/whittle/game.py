from whittle.classes import Node
from whittle.words import fetch_words, lookup_word, select_words, slice


def create_possible_paths(string):
    if not string:
        return None

    possibilities = find_replaceable_indicies(string)
    if not possibilities:
        return None
    else:
        for node in possibilities:
            new_s = slice(string, node.value)
            node.children = create_possible_paths(new_s)

    return possibilities


def find_replaceable_indicies(string):
    """
    Takes a string and finds all indexes that can be replaced and keep the string valid.
    The string is valid if it is one or two real words.
    ex. if the string is bing add | index 1 would be invalid while index 3 would be valid
    bng add > bng not a real word | bin add both are real words
    """
    possibilities = []
    for i in range(len(string)):
        new = slice(string, i)
        words = new.split(" ")
        results = [lookup_word(w) for w in words]
        if all(results):
            possibilities.append(Node(i))

    return possibilities


def find_solutions(words):
    puzzle_str = f"{words[0].word} {words[1].word}"
    nodes = create_possible_paths(puzzle_str)
    if nodes is None:
        return None
    paths = format_as_paths(nodes)
    validated_paths = remove_invalid_paths(paths, puzzle_str)

    return validated_paths


def remove_invalid_paths(paths, string):
    valid_paths = []
    for sequence in paths:
        if sequence[-1] != 0:
            continue
        copy = string
        for i in sequence:
            copy = slice(copy, i)

        if copy == "":
            valid_paths.append(sequence)

    return valid_paths


def get_paths(node, previous=None):
    all = []
    if previous is None:
        previous = []
    current_path = previous
    current_path.append(node.value)
    if node.children is None:
        all.append(current_path)
        return all

    for c in node.children:
        copy = current_path.copy()
        all += get_paths(c, copy)

    return all


def format_as_paths(nodes):
    sequences = []
    for node in nodes:
        path = get_paths(node)
        sequences += path

    return sequences


def generate_whittle():
    all_words = fetch_words()
    candidates = select_words(all_words)
    result = None
    invalid = -1
    while not result:
        invalid += 1
        candidates = select_words(all_words)
        result = find_solutions(candidates) or []
        if result is not None and len(result) > 15:
            result = None

    import random as r

    print("Attempts: ", invalid)
    print(f"Words - {candidates[0]} | {candidates[1]}")
    print(f"Solution count: {len(result)}")
    for i in range(0, 3):
        print(r.choice(result))

    return {
        "whittle": f"{candidates[0]} {candidates[1]}",
        "solution_count": len(result),
        "solutions": result,
    }


if __name__ == "__main__":
    generate_whittle()
