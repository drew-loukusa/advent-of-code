# https://adventofcode.com/2021/day/10

import sys
from collections import defaultdict as dd
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    """Process the input file into a data structure for solve()"""
    return [line.rstrip() for line in open(infile)]

def solve(data):
    result = None 
    open_chars = set("([{<")
    close_to_open = {')':'(', ']':'[', '}':'{', '>':'<'}
    stack = []
    bad_char_count = dd(int)
    for line in data:
        bad_char = None 
        for char in line:
            if char in open_chars:
                stack.append(char)
                continue 
            if char not in open_chars:
                open_char = close_to_open[char]
                if open_char == stack[-1]:
                    stack.pop()
                else:
                    bad_char = char 
                    break 
        if bad_char != None:
            bad_char_count[bad_char] += 1
    
    scores = {')':3, ']': 57, '}':1197, '>':25137}
    syntax_error_score = 0
    for char in bad_char_count:
        syntax_error_score += scores[char] * bad_char_count[char]
    
    return syntax_error_score

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 10
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day10ex.txt", ans=26397)

    # Run question 
    aoc.test("day10.txt", ans=316851, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
