# https://adventofcode.com/2021/day/14

import sys
from collections import defaultdict as dd, Counter
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test
import part_a

def process(infile):
    """Process the input file into a data structure for solve()"""
    
    template = None 
    memo = dict()
    for line in open(infile):
        line = line.rstrip()
        if len(line) <= 0: 
            continue
        if template is None:
            template = line
        else:
            rule, _, element = line.split(' ')
            memo[rule] = rule[0] + element + rule[1]
    return template, memo

def solve(template, insert_rules, steps_to_run):
    pass
    
def main(infile):
    return solve(*part_a.process(infile), steps_to_run=40)
    
if __name__ == "__main__":
    year, day = 2021, 14
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day14ex.txt", ans=None)

    # Run question 
    aoc.test("day14.txt", ans=None, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_b = aoc.answer
