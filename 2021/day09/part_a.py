# https://adventofcode.com/2021/day/9

import sys
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    """Process the input file into a data structure for solve()"""
    return [[ int(c) for c in line.rstrip()] for line in open(infile)]

def solve(data):
    MAX_Y = len(data) - 1
    MAX_X = len(data[0]) - 1
    risk_sum = 0
    for y, row in enumerate(data):
        for x, num in enumerate(row):
            if x > 0: # Check left
                if row[x - 1] <= num:
                    continue
            if x < MAX_X: # Check right
                if row[x + 1] <= num:
                    continue
            if y > 0: # Check up
                if data[y - 1][x] <= num:
                    continue
            if y < MAX_Y: # Check down
                if data[y + 1][x] <= num:
                    continue
            risk_sum += (1 + num)
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
