# https://adventofcode.com/2021/day/10#part1

import sys
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def main(infile):
    lines = [line.rstrip() for line in open(infile)]
    result = None 
    # Problem soving go HERE
    return result 
    
if __name__ == "__main__":
    year, day = 2021, 10
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS
    aoc.test("day10ex.txt", ans=None)

    # Run question 
    aoc.test("day10.txt", ans=None, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
