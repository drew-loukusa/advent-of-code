# https://adventofcode.com/2021/day/9

import sys
from typing import List
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    """Process the input file into a data structure for solve()"""
    return [[ int(c) for c in line.rstrip()] for line in open(infile)]

def locate_low_points(matrix) -> List[tuple]:
    """
    Locate low points in a matrix. A point is considered to be a low point if all
    neighbors are greater than itself. Points on an edge only need to consider
    existing neighbors. (A corner has 2 neighbors, an edge has 3)

    Returns a list of tuples.
    """
    MAX_Y = len(matrix) - 1
    MAX_X = len(matrix[0]) - 1
    low_points = []
    for y, row in enumerate(matrix):
        for x, num in enumerate(row):
            if x > 0 and row[x - 1] <= num: # Check left
                continue
            if x < MAX_X and row[x + 1] <= num: # Check right
                continue
            if y > 0 and matrix[y - 1][x] <= num: # Check up
                continue
            if y < MAX_Y and matrix[y + 1][x] <= num: # Check down
                continue
            low_points.append((y,x))
    return low_points

def solve(matrix):
    risk_sum = 0
    for y,x in locate_low_points(matrix):
        risk_sum += (1 + matrix[y][x])
    return risk_sum

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 9
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day9ex.txt", ans=15)

    # Run question 
    aoc.test("day9.txt", ans=524, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
