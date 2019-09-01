# PART 1:
#
# Example:
# aaAA Nothing happens
#
# dabAcCaCBAcCcaDA  The first 'cC' is removed.
# dabAaCBAcCcaDA    This creates 'Aa', which is removed.
# dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
# dabCBAcaDA        No further actions can be taken.

# Seek the pair of one lowercase and one uppercase of the same character
# The order doesn't matter
# 

from typing import Tuple

sample = 'dabAcCaCBAcCcaDA'

def checker(string: str) -> bool:
    for index, char in enumerate(string):
        try:
            if abs(ord(string[index]) - ord(string[index+1])) == 32:
                return True
        except IndexError:
            return False

def polymerization(string: str) -> int:
    while checker(string):
        for index, char in enumerate(string):            
            try:
                first = string[index]
                second = string[index + 1]
                if abs(ord(first) - ord(second)) == 32:
                # if (first.lower() == second.lower()) and (first != second):
                    string = string.replace(first+second, '')
            except IndexError:
                continue

    return len(string)

assert polymerization(sample) == 10

with open('data/day5_input.txt') as f:
    entry = f.read().strip()

print(polymerization(entry))


# PART 2:
# remove all the possible units (e.g, A/a unit) and find the shortest length of polymer 
# chr(97) -> 'a', chr(97-32) -> 'A'

def removing_unit(string: str, units: Tuple[str, str]) -> str:
    for unit in units:
        string = string.replace(unit, '')
    
    return string


def find_shortest_length(string: str) -> int:
    result_dict = {}
    chars = {c.lower() for c in string}

    # for upper, lower in zip(range(97, 97+26), range(65, 65+26)):
    for char in chars:
        upper_unit = char.upper()
        lower_unit = char
        string_length = polymerization(removing_unit(string, (upper_unit, lower_unit)))
        result_dict.update({(upper_unit, lower_unit) : string_length})

    # shortest_unit_length = sorted(result_dict.items(), key=lambda x: x[1])[0]
    shortest_length = min(result_dict.values())

    return shortest_length

assert find_shortest_length(sample) == 4

# print(find_shortest_length(entry))



