# gathering all the points given into Point class which can calculate manhattan distance for every points in a grid
# make the grid
# check if some points are on the boundary of the grid
# With points that are not on the boundary, calculate the largest area

from typing import NamedTuple, List, Tuple, Dict, Counter
from collections import Counter

# PART 1:

RAW = '''1, 1
1, 6
8, 3
3, 4
5, 5
8, 9'''

LINES = RAW.split('\n')


class Point(NamedTuple):
    x: int
    y: int
    
    def manhattan_distance(self, other: 'Point') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def total_manhattan_distance(self, others: List['Point']) -> int:
        return sum(self.manhattan_distance(point) for point in others)

    @staticmethod
    def from_line(line: str) -> 'Point':
        x, y = line.split(', ')
        return Point(int(x), int(y))


def make_grid(points: List[Point]) -> Dict[Point, int]:
    min_x = min([point.x for point in points])
    max_x = max([point.x for point in points])
    min_y = min([point.y for point in points])
    max_y = max([point.y for point in points])

    grid = {}

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            this = Point(x,y)
            distances = [(this.manhattan_distance(point), idx) for idx, point in enumerate(points)]
            distances.sort()
            
            if distances[0][0] == distances[1][0]:
                grid[this] = None
            else:
                grid[this] = distances[0][1]
    
    return grid

POINTS = [Point.from_line(LINE) for LINE in LINES]
GRID = make_grid(POINTS)

def count_areas(grid: Dict[Point, int]) -> Counter:
    min_x = min([point.x for point in grid])
    max_x = max([point.x for point in grid])
    min_y = min([point.y for point in grid])
    max_y = max([point.y for point in grid])

    areas = Counter()

    boundary_idx = set()
    for point, idx in grid.items():
        if point.x in (min_x, max_x) or point.y in (min_y, max_y):
            boundary_idx.add(idx)
    
    for point, idx in grid.items():
        if idx not in boundary_idx:
            areas[idx] += 1

    return areas


print(count_areas(GRID))
print(count_areas(GRID).most_common(2))

with open('data/day6_input.txt') as f:
    points = [Point.from_line(line) for line in f]

grid = make_grid(points)

print(count_areas(grid))
print(count_areas(grid).most_common(1))

# PART 2:

def total_area_of_safe_coordinates(points: List[Point], criterion: int) -> int:
    min_x = min([point.x for point in points])
    max_x = max([point.x for point in points])
    min_y = min([point.y for point in points])
    max_y = max([point.y for point in points])

    area = 0

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            this = Point(x,y)
            distances = this.total_manhattan_distance(points)

            if distances < criterion:
                area += 1
    
    return area

assert total_area_of_safe_coordinates(POINTS, 32) == 16

print(total_area_of_safe_coordinates(points, 10000))


