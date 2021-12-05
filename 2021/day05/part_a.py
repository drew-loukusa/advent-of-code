# https://adventofcode.com/2021/day/5

import sys
from collections import defaultdict as dd
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    """Process the input file into a data structure for solve()"""
    data = []
    for line in open(infile):
        line = line.rstrip()     
        a, _, b = line.split()
        a = Point(*a.split(','))
        b = Point(*b.split(','))
        data.append((a,b))
    return data 

class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __repr__(self):
        return f"(x: {self.x}, y:{self.y})"

def dump_points(points):
    for y in range(10):
        for x in range(10):
            count = points[(x,y)]
            if count > 0:
                print(count, end='')
            else:
                print('.', end='')
        print()

def count_overlaps(data, OVERLAP_NUM=2):
    overlaps = set()
    points = dd(int)
    for a,b in data:
        if a.x != b.x and a.y != b.y:
            continue 

        # Generate points in between a and b 
        line_points = []

        # Vertical line 
        if a.x == b.x:
            start = a if a.y < b.y else b
            end = a if a.y > b.y else b
            line_points.append(start)
            for y in range(start.y + 1, end.y):
                line_points.append(Point(start.x, y))
            line_points.append(end)

        # Horizontal line 
        if a.y == b.y:
            start = a if a.x < b.x else b
            end = a if a.x > b.x else b 
            line_points.append(start)
            for x in range(start.x + 1, end.x):
                line_points.append(Point(x, start.y))
            line_points.append(end)

        for point in line_points:
            points[(point.x, point.y)] += 1

            # Check after incrementing a point if you have walked
            # over it already. If yes, add it to the overlaps set
            if points[(point.x, point.y)] >= OVERLAP_NUM:
                overlaps.add((point.x, point.y))

        #dump_points(points)

    return len(overlaps)

def main(infile):
    return count_overlaps(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 5
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day5ex.txt", ans=5)

    # Run question 
    aoc.test("day5.txt", ans=6113, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
