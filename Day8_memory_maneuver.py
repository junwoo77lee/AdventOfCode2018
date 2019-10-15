# 2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
# A----------------------------------
#     B----------- C-----------
#                      D-----

# PART I:

RAW = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
INPUT = [int(x) for x in RAW.split()]

from typing import List, NamedTuple, Tuple

class Node(NamedTuple):
    num_childs: int
    num_metadata: int
    children: List['Node']
    metadata: List[int]


def parse_node(inputs: List[int], start: int = 0) -> Tuple[Node, int]:
    
    num_childs = inputs[start]
    num_metadata = inputs[start + 1]
    start = start + 2

    children = []

    for _ in range(num_childs):
        child, start = parse_node(inputs, start)
        children.append(child)
    
    metadata = inputs[start : start + num_metadata]

    return Node(num_childs, num_metadata, children, metadata), (start + num_metadata)

ROOT, _ = parse_node(INPUT)

def add_metadata(root: Node) -> int:
    return sum(root.metadata) + sum(add_metadata(child) for child in root.children)

assert add_metadata(ROOT) == 138


with open("./data/day8_input.txt") as f:
    entries = [int(x) for x in f.read().strip().split()]

root, _ = parse_node(entries)

print(add_metadata(root))

# PART II:

def find_value_of_node(node: Node) -> int:
    value = 0
    if node.num_childs == 0:
        return sum(node.metadata)
    else:
        for index in node.metadata:
            try:
                new_node = node.children[index - 1]
                value += find_value_of_node(new_node)
            except:
                value += 0
    return value

assert find_value_of_node(ROOT) == 66

print(find_value_of_node(root))









