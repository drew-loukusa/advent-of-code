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
                tokens.pop(0)
                break 
            signal_patterns.append(tk)
        output_value = tokens 
        data.append((signal_patterns, output_value))
    return data 

def solve(data):
    segments = {
        0: set("abcefg"), 1: set("cf"), 2: set("acdeg"), 3: set("acdfg"), 4: set("bcdf"),
        5: set("abdfg"), 6: set("abdefg"), 7: set("acf"), 8: set("abcdefg"), 9: set("abcdfg")
    }

    segments_used = {2:(1), 3:(7), 4:(4), 5:(2,3,5), 6:(0, 6, 9), 7:(8) }
    translation_table = {}

    for entry in data:
        segment_pool = "abcdefg"
        segment_patterns = entry[0]
        output_values = entry[1]
        sorted_patterns = sorted(segment_patterns, key=len)
        for pattern in sorted_patterns:
            if len(pattern) == 1:
                pass 
            if len(pattern) == 4:
                pass
            if len(pattern) == 7:
                pass 
            if len(pattern) == 8:
                pass 

    print(data)


def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 8
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day8ex.txt", ans=26)

    # Run question 
    aoc.test("day8.txt", ans=-1, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
