# https://adventofcode.com/2021/day/15

import sys
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    """Process the input file into a data structure for solve()"""
    return [[int(n) for n in line.rstrip()] for line in open(infile) ] 

def solve(m):
    m[0][0] = 0
    for y, row in enumerate(m):
        for x, _ in enumerate(row):
            up, left = None, None 
            if x > 0:
                left = m[y][x - 1]
            if y > 0: 
                up = m[y - 1][x]

            if up is not None and left is not None:
                m[y][x] += min(left, up)
            elif up is not None:
                m[y][x] += up 
            elif left is not None:
                m[y][x] += left
    
    return m[-1][-1] 

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 15
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day15ex.txt", ans=40)

    # Run question 
    aoc.test("day15.txt", ans=811, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
