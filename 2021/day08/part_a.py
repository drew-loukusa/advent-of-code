# https://adventofcode.com/2021/day/8

import sys
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    """Process the input file into a data structure for solve()"""
    data = []
    for line in open(infile):
        signal_patterns = []
        tokens = line.rstrip().split(' ')
        while len(tokens) > 0:
            tk = tokens.pop(0)
            if tk == '|':
                break 
            signal_patterns.append(tk)
        output_value = tokens 
        data.append((signal_patterns, output_value))
    return data 

def solve(data):
    appearance_count = 0
    for entry in data:
        output_values = entry[1]
        for pattern in output_values:
            plen = len(pattern)
            # Segment count for 1, 4, 7, 8
            if plen in {2,4,3,7}:
                appearance_count += 1
    return appearance_count


def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 8
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day8ex.txt", ans=26)

    # Run question 
    aoc.test("day8.txt", ans=383, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
