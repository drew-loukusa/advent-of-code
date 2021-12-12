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
    br = {')':'(', ']':'[', '}':'{', '>':'<'}
    stack = []
    corrupted_chars = dd(int)
    for line in data:
        corrupted_char = None 
        for char in line:
            if char in open_chars:
                stack.append(char)
                continue 
            if char not in open_chars:
                matching_open_char = br[char]
                if matching_open_char == stack[-1]:
                    stack.pop()
                else:
                    corrupted_char = char 
                    break 
        if corrupted_char != None:
            corrupted_chars[corrupted_char] += 1
    
    scores = {')':3, ']': 57, '}':1197, '>':25137}
    syntax_error_score = 0
    for char in corrupted_chars:
        syntax_error_score += scores[char] * corrupted_chars[char]
    
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
    aoc.test("day10.txt", ans=-1, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
