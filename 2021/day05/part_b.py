# https://adventofcode.com/2021/day/5

import sys
from collections import defaultdict as dd
from typing import List, overload
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test
from part_a import Point

def generate_segments(infile) -> List[List[Point]]:
    """
    Generate a list of segments to be walked over later.
    A segment is a list of Point objects.
    """
    segments = []
    for line in open(infile):
        line = line.rstrip()     
        a, _, b = line.split()
        a = Point(*a.split(','))
        b = Point(*b.split(','))
        segments.append(make_segment(a,b))
    return segments 

def make_segment(a: Point, b: Point):
    segment = []
    # Vertical line 
    if a.x == b.x:
        start = a if a.y < b.y else b
        end = a if a.y > b.y else b
        for y in range(start.y, end.y + 1):
            segment.append(Point(start.x, y))
        

    # Horizontal line 
    elif a.y == b.y:
        start = a if a.x < b.x else b
        end = a if a.x > b.x else b 
        for x in range(start.x, end.x + 1):
            segment.append(Point(x, start.y))
        

    # Diagonal line
    else:
        start = a if a.x < b.x else b 
        end = a if a.x > b.x else b 
        y = start.y 
        for x in range(start.x, end.x + 1):
            segment.append(Point(x, y))
            if start.y > end.y:
                y -= 1
            else:
                y += 1
    return segment

def count_overlaps(segments: List[List[Point]], overlap_minimum=2):
    overlaps = set()
    points = dd(int)
    for segment in segments:
        for point in segment:
            points[(point.x, point.y)] += 1

            # Check after incrementing a point if you have walked
            # over it already. If yes, add it to the overlaps set
            if points[(point.x, point.y)] >= overlap_minimum:
                overlaps.add((point.x, point.y))

        #dump_points(points)

    return len(overlaps)



#============================================================================#
#                           Improved algorithm                               #
#============================================================================#

# Count the number of times you walk on a given point in a line segment WHILE 
# you generate said line segment. 
# Previously I was generating the segments all at once, then walking over them
# in a seperate step. 
# I walk over them to count each point, but I can do that WHEN I MAKE the segment.

def read_pairs(infile):
    """Generator function that gets the next pair coords defining a line segment"""
    for line in open(infile):
        line = line.rstrip()     
        a, _, b = line.split()
        a = Point(*a.split(','))
        b = Point(*b.split(','))
        yield (a,b)

def walk_segment(a: Point, b: Point, points: dict, overlaps: set):   
    # Vertical line 
    if a.x == b.x:
        start = a if a.y < b.y else b
        end = a if a.y > b.y else b
        for y in range(start.y, end.y + 1):
            p = Point(start.x, y)
            points[(p.x, p.y)] += 1

            # Check after incrementing a point if you have walked
            # over it already. If yes, add it to the overlaps set
            if points[(p.x, p.y)] >= 2:
                overlaps.add((p.x, p.y))
        

    # Horizontal line 
    elif a.y == b.y:
        start = a if a.x < b.x else b
        end = a if a.x > b.x else b 
        for x in range(start.x, end.x + 1):
            p = Point(x, start.y)
            points[(p.x, p.y)] += 1

            # Check after incrementing a point if you have walked
            # over it already. If yes, add it to the overlaps set
            if points[(p.x, p.y)] >= 2:
                overlaps.add((p.x, p.y))


    # Diagonal line
    else:
        start = a if a.x < b.x else b 
        end = a if a.x > b.x else b 
        y = start.y 
        for x in range(start.x, end.x + 1):
            p = Point(x, y)
            if start.y > end.y:
                y -= 1
            else:
                y += 1
            points[(p.x, p.y)] += 1

            # Check after incrementing a point if you have walked
            # over it already. If yes, add it to the overlaps set
            if points[(p.x, p.y)] >= 2:
                overlaps.add((p.x, p.y))

def count_overlaps_while_generating_segments(infile):
    # Dict of point, {(x,y) -> count} , for tracking how many times we "step" on each point
    points = dd(int)
    # Set where points are placed once their count increases to 2 or above 
    overlap = set()
    for a,b in read_pairs(infile):
        walk_segment(a, b, points, overlap)
    return len(overlap)

def main(infile):
    # return count_overlaps(generate_segments(infile))
    return count_overlaps_while_generating_segments(infile)
    
if __name__ == "__main__":
    year, day = 2021, 5
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day5ex.txt", ans=12)

    # Run question 
    aoc.test("day5.txt", ans=20373, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_b = aoc.answer
