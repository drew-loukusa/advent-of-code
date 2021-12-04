# https://adventofcode.com/2021/day/3

import sys
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test
from collections import defaultdict as dd 

def process(infile):
    """Process the input file into a data structure for solve()"""
    return [line.rstrip() for line in open(infile)]

def solve(data):
    gamma, epsilon = 0,0
    bits = dd(int)
    for bin_str in data:
        for i,bit in enumerate(bin_str):
            if bit == '0':
                bits[i] -= 1
            elif bit == '1':
                bits[i] += 1
    
    gamma, epsilon = "", ""
    for i in range(len(bits)):
        if bits[i] < 0:
            gamma += "0"
            epsilon += "1"
        elif bits[i] > 0:
            gamma += "1"
            epsilon += "0"
    gamma, epsilon = int(gamma, base=2), int(epsilon, base=2)

    #print(gamma, epsilon)

    return gamma, epsilon

def main(infile):
    g,e = solve(process(infile))
    return g * e
    
if __name__ == "__main__":
    year, day = 2021, 3
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day3ex.txt", ans=198)

    # Run question 
    aoc.test("day3.txt", ans=3969000, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
