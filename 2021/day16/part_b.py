# https://adventofcode.com/2021/day/16

import sys
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test
from part_a import process, Packet, process_packet

def solve(bin_str):   
    # Process the 'packet' (and any sub packets)
    top_level_packet: Packet = process_packet(bin_str)[1]

    return top_level_packet.value

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 16
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("ex0.txt", ans=15)
    aoc.test("ex1.txt", ans=46)
    aoc.test("ex2.txt", ans=46)
    aoc.test("ex3.txt", ans=54)

    # Run question 
    aoc.test("puzzle_input.txt", ans=124921618408, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_b = aoc.answer
