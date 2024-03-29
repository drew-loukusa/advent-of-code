# Sonar sweep part 1
# https://adventofcode.com/2021/day/1#part1

import sys
from typing import List
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    return [int(line.rstrip()) for line in open(infile)]

def solve(data: List[int]):
    num_increases = 0
    last = data[0]
    for cur in data[1:]:
        if cur > last:
            num_increases += 1
        last = cur
    return num_increases

def main(infile):
    return solve(process(infile))

if __name__ == "__main__":
    # Setup
    year, day = 2021, 1
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS
    aoc.test("day1ex.txt", ans=7)

    # Run question 
    aoc.test("day1.txt", ans=1548, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
