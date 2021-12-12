# https://adventofcode.com/2021/day/10

import sys
from collections import defaultdict as dd
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

OPEN_CHARS = set("([{<")
CLOSE_TO_OPEN = {')':'(', ']':'[', '}':'{', '>':'<'}
OPEN_TO_CLOSE = {v:k for k,v in CLOSE_TO_OPEN.items()}

def process(infile):
    """Process the input file into a data structure for solve()"""
    return [line.rstrip() for line in open(infile)]

def process_line(line) -> list:
    stack = []
    for char in line:
        if char in OPEN_CHARS:
            stack.append(char)
            continue 
        if char not in OPEN_CHARS:
            open_char = CLOSE_TO_OPEN[char]
            if open_char == stack[-1]:
                stack.pop()
            # If the line is corrupted, return an empty list
            else:
                return None
    return stack 

def solve(data):
    scores = []
    points = {')':1, ']':2, '}':3, '>':4}
    for line in data:
        stack = process_line(line)
        # Skip corrupted lines
        if stack is None: continue
        # Calculate what is needed to complete the line:
        print(end='')
        line_score = 0
        while len(stack) > 0:
            closeing_char = OPEN_TO_CLOSE[stack.pop()]
            line_score = line_score * 5 + points[closeing_char]
        scores.append(line_score)
    
    length = len(scores)
    index = length//2
    sorted_scores = sorted(scores)
    return sorted_scores[index]

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 10
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day10ex.txt", ans=288957)

    # Run question 
    aoc.test("day10.txt", ans=2182912364, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_b = aoc.answer
