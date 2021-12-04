# https://adventofcode.com/2021/day/3

import sys
from collections import defaultdict as dd 
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    """Process the input file into a data structure for solve()"""
    return [line.rstrip() for line in open(infile)]

def most_common_bit(data, index):
    mcb = 0
    for bin_str in data:
        bit = bin_str[index]
        if bit == '0':
            mcb -= 1
        elif bit == '1':
            mcb += 1

    if mcb == 0:
        return None 
    return '0' if mcb < 0 else '1'

def select(data, mcb, index, mode):
    if mcb == None:
        mcb = '1'
    lcb = '0' if mcb == '1' else '1'
    new_data = []
    for bin_str in data:
        if mode == "mcb" and bin_str[index] == mcb:
            new_data.append(bin_str)
        
        if mode == "lcb" and bin_str[index] == lcb:
            new_data.append(bin_str)
    return new_data 

def solve(data):
    o2_genR, co2_scrubR = 0,0
    
    cur_data = data[:]
    for i in range(len(data[0])):
        if len(cur_data) == 1:
            break
        mcb = most_common_bit(cur_data, i)
        cur_data = select(cur_data, mcb, i, mode="mcb")
    
    o2_genR = int(''.join(cur_data[0]), base=2)

    cur_data = data[:]
    for i in range(len(data[0])):
        if len(cur_data) == 1:
            break
        mcb = most_common_bit(cur_data, i)
        cur_data = select(cur_data, mcb, i, mode="lcb")
    
    co2_scrubR = int(''.join(cur_data[0]), base=2)

    return o2_genR * co2_scrubR

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 3
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day3ex.txt", ans=230)

    # Run question 
    aoc.test("day3.txt", ans=4267809, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_b = aoc.answer
