# https://adventofcode.com/2021/day/6

import sys
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

DAYS_TO_RUN = 80
CYCLE_LENGTH = 6 # 0 is included as a valid value, so this wolud be 7 
INITIAL_CYCLE_LENGTH = 8 # ditto, would be 9

def process(infile):
    """Process the input file into a data structure for solve()"""
    return [int(n) for n in open(infile).readline().split(',')]

def solve(school: list):
    # Naive brute force solution
    for _ in range(DAYS_TO_RUN):
        new_fishes = []
        for i, fish in enumerate(school):
            if fish == 0:
                new_fishes.append(INITIAL_CYCLE_LENGTH)
                school[i] = CYCLE_LENGTH
            else:
                school[i] -= 1
        school.extend(new_fishes)
    return len(school)

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 6
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day6ex.txt", ans=5934)

    # Run question 
    aoc.test("day6.txt", ans=-1, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
