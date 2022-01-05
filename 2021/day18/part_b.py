# https://adventofcode.com/2021/day/18

import sys
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    """Process the input file into a data structure for solve()"""
    return [line.rstrip() for line in open(infile)]

def solve(data):
    result = None 
    # Problem soving go HERE
    return result 

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 18
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("ex0.txt", ans=None)

    # Run question 
    aoc.test("puzzle_input.txt", ans=None, save_answer=True)
    
    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_b = aoc.answer
