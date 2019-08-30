from typing import NamedTuple, Tuple, Iterator, List, Dict
import re
from collections import Counter


regex = '#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$'
coord = Tuple[int, int]

class Rectangle(NamedTuple): # inheritance from NamedTuple
    id: int
    x_left: int
    x_top: int
    width: int
    height: int

## Also Working ##
# class Rectangle():
#     def __init__(self, id, x_l, x_t, w, h):
#         self.id = id
#         self.x_left = x_l
#         self.x_top = x_t
#         self.width = w
#         self.height = h

    @staticmethod
    def from_claim(claim: str) -> 'Rectangle':
        # sample claim -> #21 @ 573,694: 21x19
        id, x_left, x_top, width, height = [int(element) for element in re.match(regex, claim).groups()]
        return Rectangle(id, x_left, x_top, width, height)
    

    def all_coordiantes(self) -> Iterator[coord]:
        for x in range(self.x_left, self.x_left + self.width):
            for y in range(self.x_top, self.x_top + self.height):
                yield (x, y)


assert Rectangle.from_claim('#21 @ 573,694: 21x19') == Rectangle(21, 573, 694, 21, 19)


def coverage(rectangles: List[Rectangle]) -> Dict[coord, int]:

    counts = Counter()

    for rectangle in rectangles:
        for point in rectangle.all_coordiantes():
            counts[point] += 1

    return counts

def multiple_claims(claims: List[str]) -> int:
      
    rectangles = [Rectangle.from_claim(claim) for claim in claims]

    counts = coverage(rectangles)

    return len([count for count in counts.values() if count >= 2])


# Test claims
test_list = ['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2']
assert multiple_claims(test_list) == 4

# Actual claims
with open('./data/day3_input.txt') as f:
    claims = [line.strip() for line in f]

print(multiple_claims(claims))


def find_the_one(claims: List[str]) -> int: # The id number

    rectangles = [Rectangle.from_claim(claim) for claim in claims]
    counts = coverage(rectangles)

    good_rectangles =[rectangle
                      for rectangle in rectangles
                      if all(
                             [counts[coord] == 1 for coord in rectangle.all_coordiantes()]
                             )
                     ]
    assert len(good_rectangles) == 1

    return good_rectangles[0].id


print(find_the_one(claims))


    # My code for part 2 #
    
    # counts = {k:v for k, v in counts.items() if v >= 2}
    # rectangles = [Rectangle.from_claim(claim) for claim in claims]

    # for rectangle in rectangles:
        
    #     overlapped = 0
        
    #     for coord in rectangle.all_coordiantes():
    #         if coord in counts.keys():
    #             overlapped += 1
    #     if not overlapped:
    #         return rectangle.id

