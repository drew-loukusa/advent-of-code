# https://adventofcode.com/2021/day/2

import sys
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    return [line.rstrip() for line in open(infile)]

def solve(data):
    hpos, depth = 0,0 
    
    for line in data:
        cmd, amnt = line.split(' ')
        amnt = int(amnt)
        # TODO Upgrade Python version to 3.10 so you can use structural pattern matching here 
        # Will have to install 3.10, remove 3.96 and then re-init the env

        if cmd == "forward": 
            hpos += amnt
        elif cmd == "down": 
            depth += amnt
        elif cmd == "up": 
            depth -= amnt

    return hpos * depth

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 2
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS
    aoc.test("day2ex.txt", ans=150)

    # Run question 
    aoc.test("day2.txt", ans=1635930, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
